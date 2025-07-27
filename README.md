# 🎲 Bingo Card Generator 2.0 (BCG_2.0)

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Concluído-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-informational?style=for-the-badge)

Uma aplicação de desktop moderna e intuitiva para gerar e exportar centenas de cartelas de bingo personalizadas em formato PDF, com base em modelos SVG e dados de planilhas Excel.

### Sobre o Projeto

O Bingo Card Generator 2.0 foi criado para resolver um problema comum em eventos: a necessidade de gerar um grande volume de cartelas de bingo únicas de forma rápida e com um design personalizado. A aplicação combina um backend robusto para processamento de dados com uma interface gráfica limpa e amigável.

O projeto foi desenvolvido com foco em:
- **Eficiência:** Geração em lote a partir de uma planilha, com uma barra de progresso para acompanhar o processo.
- **Flexibilidade:** Permite que o usuário crie seu próprio design de cartela usando um modelo SVG, que pode ser editado em softwares como o CorelDRAW ou Inkscape.
- **Interface Intuitiva:** Construído com `CustomTkinter` para uma experiência de usuário moderna e agradável.
- **Segurança:** O usuário pode cancelar a geração a qualquer momento de forma segura, sem corromper os arquivos.

---

### ✨ Principais Funcionalidades

- **Geração a partir de Planilhas:** Importa os dados das cartelas diretamente de um arquivo Excel (`.xlsx`), usando a coluna `N` como identificador.
- **Design via Modelo SVG:** Utiliza um arquivo SVG como template, substituindo marcadores de texto (ex: `{{B1}}`, `{{N}}`) pelos dados da planilha para criar cada cartela.
- **Exportação em Lote para PDF:** Gera todas as cartelas da planilha e as consolida em um único arquivo PDF, pronto para impressão.
- **Interface Gráfica Completa:**
    - Botões para selecionar o arquivo Excel e o modelo SVG.
    - Barra de progresso visual que mostra o andamento da geração.
    - Botão de "Cancelar" para interromper o processo com segurança.
    - Feedback em tempo real através de um console de status na própria interface.

---

### 🖼️ Capturas de Tela

<p align="center">
  <img src="https://github.com/Vectorgg15/BCG_2.0/raw/main/assets/Screenshot_BCG_2.0.png" alt="Interface principal" width="700"/>
</p>

---

### 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **CustomTkinter:** Para a construção da interface gráfica moderna.
- **Pandas:** Para a leitura e manipulação eficiente dos dados da planilha Excel.
- **CairoSVG:** Para converter os modelos SVG em formato PNG.
- **PyPDF2:** Para unir as cartelas geradas em um único arquivo PDF.
- **Pillow (PIL):** Para o processamento de imagens intermediário.

---

### 🚀 Como Executar o Projeto

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/Vectorgg15/BCG_2.0.git](https://github.com/Vectorgg15/BCG_2.0.git)
    cd BCG_2.0
    ```

2.  **Crie e ative um ambiente virtual (Recomendado):**
    ```bash
    python -m venv venv
    # No Windows
    venv\Scripts\activate
    # No macOS/Linux
    # source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute o aplicativo:**
    ```bash
    python gerador_cartela_2.0.py
    ```
    *Observação: Certifique-se de ter um arquivo de modelo (`.svg`) e uma planilha de dados (`.xlsx`) prontos para usar no programa.*

---

### 📄 Licença

Este projeto está sob a Licença MIT.

**Desenvolvido por Victor Manuel com 💙**
