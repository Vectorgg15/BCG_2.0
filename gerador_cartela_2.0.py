import customtkinter as ctk
from tkinter import filedialog
import pandas as pd
import os
import sys  # Import necessário para a função resource_path
from io import BytesIO
from PyPDF2 import PdfWriter, PdfReader
import cairosvg
import re
from PIL import Image
import threading
import queue

# --- FUNÇÃO PARA ENCONTRAR ARQUIVOS EMPACOTADOS ---
def resource_path(relative_path):
    """ Retorna o caminho absoluto para o recurso, funcionando tanto no modo dev quanto no PyInstaller """
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Se não estiver rodando como .exe, use o caminho normal do script
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# --- Configurações globais e Paleta de Cores ---
ctk.set_appearance_mode("light")
LOGO_RED = "#d40000"
LOGO_RED_HOVER = "#a80000"
LOGO_BLUE = "#1a237e"
LOGO_BLUE_ACCENT = "#534bae"
CANCEL_GRAY = "#757575"
CANCEL_GRAY_HOVER = "#616161"
BACKGROUND_CTK_COLOR = "#f0f2f5"
TEXT_CTK_COLOR = "#333333"

# --- Classe para a MessageBox Personalizada ---
class CustomMessageBox(ctk.CTkToplevel):
    def __init__(self, master, title, message, msg_type="info"):
        super().__init__(master)
        self.master = master
        self.title(title)
        self.transient(master)
        self.grab_set()
        self.resizable(False, False)

        bg_color_map = {"info": "#e3f2fd", "success": "#e8f5e9", "warning": "#fffde7", "error": "#ffebee"}
        text_color_map = {"info": "#0d47a1", "success": "#1b5e20", "warning": "#f57f17", "error": "#b71c1c"}
        char_icon_map = {"info": "ℹ️", "success": "✔️", "warning": "⚠️", "error": "❌"}

        dialog_bg = bg_color_map.get(msg_type, BACKGROUND_CTK_COLOR)
        dialog_text_color = text_color_map.get(msg_type, TEXT_CTK_COLOR)
        dialog_char_icon = char_icon_map.get(msg_type, "")

        self.configure(fg_color=dialog_bg)
        frame = ctk.CTkFrame(self, fg_color=dialog_bg)
        frame.pack(padx=20, pady=20, expand=True, fill="both")
        icon_label = ctk.CTkLabel(frame, text=dialog_char_icon, font=ctk.CTkFont(family="Arial", size=24), text_color=dialog_text_color, fg_color=dialog_bg)
        icon_label.pack(pady=(0, 10))
        msg_label = ctk.CTkLabel(frame, text=message, text_color=dialog_text_color, font=ctk.CTkFont(family="Arial", size=12, weight="bold" if msg_type in ["error", "warning"] else "normal"), wraplength=300, justify="center", fg_color=dialog_bg)
        msg_label.pack(pady=10)
        ok_button = ctk.CTkButton(frame, text="OK", command=self.destroy, fg_color=LOGO_BLUE, hover_color=LOGO_BLUE_ACCENT, font=ctk.CTkFont(family="Arial", size=12, weight="bold"))
        ok_button.pack(pady=10)
        self.update_idletasks()
        x = master.winfo_x() + (master.winfo_width() // 2) - (self.winfo_width() // 2)
        y = master.winfo_y() + (master.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BCG_2.0")
        self.geometry("700x550")
        self.resizable(False, False)

        self.df = None
        self.excel_file_path = ctk.StringVar()
        self.template_svg_path = ctk.StringVar()
        self.cancel_flag = threading.Event()
        self.progress_queue = queue.Queue()

        # --- UI ---
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(pady=10, padx=20, fill="x")
        self.title_label = ctk.CTkLabel(top_frame, text="🎲 Bingo Card Generator 2.0 (BCG_2.0)", font=ctk.CTkFont(family="Arial", size=18, weight="bold"), text_color=LOGO_BLUE)
        self.title_label.pack()
        
        file_frame = ctk.CTkFrame(self, fg_color="transparent")
        file_frame.pack(pady=5, padx=20, fill="x")
        file_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(file_frame, text="Planilha Excel:", font=ctk.CTkFont(family="Arial", size=12), text_color=LOGO_BLUE).grid(row=0, column=0, sticky="w", padx=5)
        ctk.CTkEntry(file_frame, textvariable=self.excel_file_path, state="readonly", border_color=LOGO_BLUE_ACCENT).grid(row=0, column=1, sticky="ew")
        self.browse_excel_btn = ctk.CTkButton(file_frame, text="Procurar...", width=100, command=self._browse_excel_file, fg_color=LOGO_BLUE, hover_color=LOGO_BLUE_ACCENT)
        self.browse_excel_btn.grid(row=0, column=2, padx=5)

        ctk.CTkLabel(file_frame, text="Modelo SVG:", font=ctk.CTkFont(family="Arial", size=12), text_color=LOGO_BLUE).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ctk.CTkEntry(file_frame, textvariable=self.template_svg_path, state="readonly", border_color=LOGO_BLUE_ACCENT).grid(row=1, column=1, sticky="ew", pady=5)
        self.browse_svg_btn = ctk.CTkButton(file_frame, text="Procurar...", width=100, command=self._browse_svg_file, fg_color=LOGO_BLUE, hover_color=LOGO_BLUE_ACCENT)
        self.browse_svg_btn.grid(row=1, column=2, padx=5, pady=5)
        
        self.load_btn = ctk.CTkButton(file_frame, text="Carregar Planilha", command=self._load_dataframe, fg_color=LOGO_BLUE, hover_color=LOGO_BLUE_ACCENT)
        self.load_btn.grid(row=2, column=0, columnspan=3, pady=10)
        
        generation_main_frame = ctk.CTkFrame(self, fg_color="transparent")
        generation_main_frame.pack(pady=10, padx=15, fill="both", expand=True)
        
        self.interval_frame = ctk.CTkFrame(generation_main_frame, border_width=1, border_color=LOGO_BLUE_ACCENT)
        self.interval_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        self.interval_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(self.interval_frame, text="Gerar por Intervalo", font=ctk.CTkFont(family="Arial", size=12, weight="bold"), text_color=LOGO_BLUE).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=10)
        ctk.CTkLabel(self.interval_frame, text="Cartela Inicial:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_inicio = ctk.CTkEntry(self.interval_frame)
        self.entry_inicio.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        ctk.CTkLabel(self.interval_frame, text="Cartela Final:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_fim = ctk.CTkEntry(self.interval_frame)
        self.entry_fim.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.interval_btn = ctk.CTkButton(self.interval_frame, text="GERAR POR INTERVALO", command=self._gerar_por_intervalo, fg_color=LOGO_RED, hover_color=LOGO_RED_HOVER)
        self.interval_btn.grid(row=3, column=0, columnspan=2, pady=15)

        self.list_frame = ctk.CTkFrame(generation_main_frame, border_width=1, border_color=LOGO_BLUE_ACCENT)
        self.list_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        self.list_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(self.list_frame, text="Gerar por Lista Específica", font=ctk.CTkFont(family="Arial", size=12, weight="bold"), text_color=LOGO_BLUE).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=10)
        ctk.CTkLabel(self.list_frame, text="Nº das Cartelas:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_lista = ctk.CTkEntry(self.list_frame, placeholder_text="Ex: 5, 23, 112")
        self.entry_lista.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        ctk.CTkLabel(self.list_frame, text="").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.list_btn = ctk.CTkButton(self.list_frame, text="GERAR CARTELAS ESPECÍFICAS", command=self._gerar_por_lista, fg_color=LOGO_RED, hover_color=LOGO_RED_HOVER)
        self.list_btn.grid(row=3, column=0, columnspan=2, pady=15)
        
        status_frame = ctk.CTkFrame(self, fg_color="transparent")
        status_frame.pack(side=ctk.BOTTOM, fill="x", pady=5, padx=20)
        self.progress_label = ctk.CTkLabel(status_frame, text="Pronto para gerar.", font=ctk.CTkFont(family="Arial", size=10))
        self.progress_label.pack(side="left")
        self.cancel_btn = ctk.CTkButton(status_frame, text="Cancelar Geração", command=self._cancelar_geracao, fg_color=CANCEL_GRAY, hover_color=CANCEL_GRAY_HOVER, state="disabled")
        self.cancel_btn.pack(side="right")

        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.pack(side=ctk.BOTTOM, fill="x", pady=(0, 10))
        try:
            # USA A FUNÇÃO resource_path PARA ENCONTRAR A LOGO
            logo_path = resource_path("assets/Logo_Paróquia_ Alta Definição.png")
            logo_image = ctk.CTkImage(Image.open(logo_path), size=(67, 85))
            logo_label = ctk.CTkLabel(footer_frame, image=logo_image, text="")
            logo_label.pack()
        except FileNotFoundError:
            print("AVISO: Arquivo de logo 'Logo_Paróquia_ Alta Definição.png' não encontrado.")
        except Exception as e:
            print(f"Erro ao carregar a logo: {e}")
        self.signature_label = ctk.CTkLabel(footer_frame, text="por Victor Manuel", font=ctk.CTkFont(family="Arial", size=8), text_color="#666666")
        self.signature_label.pack()
        
        # Inicia o monitoramento da fila de progresso
        self._process_queue()

    def _toggle_ui_state(self, is_generating):
        state = "disabled" if is_generating else "normal"
        self.browse_excel_btn.configure(state=state)
        self.browse_svg_btn.configure(state=state)
        self.load_btn.configure(state=state)
        self.interval_btn.configure(state=state)
        self.list_btn.configure(state=state)
        self.cancel_btn.configure(state="normal" if is_generating else "disabled")

    def _cancelar_geracao(self):
        self.progress_label.configure(text="Cancelando...")
        self.cancel_flag.set()
        
    def _process_queue(self):
        try:
            message = self.progress_queue.get_nowait()
            msg_type, data = message

            if msg_type == "progress":
                self.progress_label.configure(text=data)
            elif msg_type == "done":
                self.progress_label.configure(text="Pronto.")
                self._toggle_ui_state(False)
                self._show_custom_messagebox("Sucesso!", f"PDF gerado com sucesso!\nArquivo: '{data}'", "success")
            elif msg_type == "cancelled":
                self.progress_label.configure(text="Geração Cancelada.")
                self._toggle_ui_state(False)
            elif msg_type == "error":
                self.progress_label.configure(text="Erro na geração.")
                self._toggle_ui_state(False)
                self._show_custom_messagebox("Erro Inesperado", f"Ocorreu um erro durante a geração:\n{data}", "error")
        
        except queue.Empty:
            pass
        finally:
            self.after(100, self._process_queue)

    def _gerar_pdf_base(self, indices_para_gerar, nome_arquivo_saida):
        if self.df is None: return self._show_custom_messagebox("Erro", "A planilha não foi carregada.", "error")
        template_path = self.template_svg_path.get()
        if not template_path: return self._show_custom_messagebox("Erro", "Selecione um arquivo de modelo SVG.", "error")
        if not os.path.exists(template_path): return self._show_custom_messagebox("Erro", f"Modelo '{os.path.basename(template_path)}' não encontrado.", "error")
        
        self.cancel_flag.clear()
        self._toggle_ui_state(is_generating=True)
        self.progress_label.configure(text="Iniciando geração...")
        
        thread = threading.Thread(target=self._worker_gerar_pdf, args=(indices_para_gerar, nome_arquivo_saida, template_path))
        thread.start()

    def _worker_gerar_pdf(self, indices_para_gerar, nome_arquivo_saida, template_path):
        try:
            with open(template_path, 'r', encoding='utf-8-sig') as f:
                template_content = f.read()
            
            pdf_writer = PdfWriter()
            total_cartelas = len(indices_para_gerar)
            
            for count, i in enumerate(indices_para_gerar):
                if self.cancel_flag.is_set():
                    self.progress_queue.put(("cancelled", None))
                    return

                cartela_data = self.df.iloc[i]
                progress_text = f"Processando {count + 1}/{total_cartelas} (Cartela N° {cartela_data['N']})..."
                self.progress_queue.put(("progress", progress_text))
                
                svg_final_content = template_content
                for col_name, value in cartela_data.items():
                    placeholder_sem_chaves = str(col_name).upper()
                    valor_final = str(value)
                    if placeholder_sem_chaves != 'N' and valor_final.isdigit() and len(valor_final) == 1:
                        valor_final = f"0{valor_final}"
                    svg_final_content = svg_final_content.replace(f"{{{{{placeholder_sem_chaves}}}}}", valor_final)

                pdf_page_bytes = BytesIO()
                cairosvg.svg2pdf(bytestring=svg_final_content.encode('utf-8'), write_to=pdf_page_bytes)
                pdf_page_bytes.seek(0)
                pdf_writer.add_page(PdfReader(pdf_page_bytes).pages[0])
            
            with open(nome_arquivo_saida, "wb") as f:
                pdf_writer.write(f)
            
            self.progress_queue.put(("done", nome_arquivo_saida))

        except Exception as e:
            print(f"ERRO NA THREAD DE GERAÇÃO: {e}")
            self.progress_queue.put(("error", str(e)))
        
    def _gerar_por_intervalo(self):
        try:
            inicio = int(self.entry_inicio.get())
            fim = int(self.entry_fim.get())
        except ValueError: return self._show_custom_messagebox("Erro", "Valores de início e fim devem ser números.", "error")
        
        numeros_no_intervalo = list(range(inicio, fim + 1))
        indices = self.df.index[self.df['N'].isin(numeros_no_intervalo)].tolist()
        if not indices: return self._show_custom_messagebox("Aviso", f"Nenhuma cartela com número entre {inicio} e {fim} foi encontrada.", "warning")
        self._gerar_pdf_base(indices, "cartelas_por_intervalo.pdf")

    def _gerar_por_lista(self):
        numeros_str = self.entry_lista.get()
        if not numeros_str: return self._show_custom_messagebox("Aviso", "Digite os números das cartelas para gerar.", "warning")
        
        try:
            numeros_desejados = {int(n.strip()) for n in numeros_str.split(',') if n.strip()}
        except ValueError: return self._show_custom_messagebox("Erro", "Digite apenas números separados por vírgula.", "error")
        
        indices = self.df.index[self.df['N'].isin(numeros_desejados)].tolist()
        if not indices: return self._show_custom_messagebox("Aviso", "Nenhuma das cartelas especificadas foi encontrada.", "warning")
        self._gerar_pdf_base(indices, "cartelas_especificas.pdf")
        
    def _show_custom_messagebox(self, title, message, msg_type="info"):
        CustomMessageBox(self, title, message, msg_type)

    def _browse_excel_file(self):
        path = filedialog.askopenfilename(title="Selecionar Planilha Excel", filetypes=[("Excel", "*.xlsx;*.xls")])
        if path: self.excel_file_path.set(path)

    def _browse_svg_file(self):
        path = filedialog.askopenfilename(title="Selecionar Modelo SVG", filetypes=[("SVG", "*.svg")])
        if path: self.template_svg_path.set(path)

    def _load_dataframe(self):
        path = self.excel_file_path.get()
        if not path: return self._show_custom_messagebox("Aviso", "Selecione um arquivo Excel.", "warning")
        try:
            self.df = pd.read_excel(path)
            self.df.columns = self.df.columns.str.strip().str.upper()
            if 'N' not in self.df.columns:
                self._show_custom_messagebox("Erro", "Coluna 'N' não encontrada na planilha.", "error")
                self.df = None
                return
            self._show_custom_messagebox("Sucesso!", f"Planilha '{os.path.basename(path)}' carregada!", "success")
        except Exception as e: self._show_custom_messagebox("Erro", f"Não foi possível carregar a planilha:\n{e}", "error")


if __name__ == "__main__":
    app = App()
    app.mainloop()
