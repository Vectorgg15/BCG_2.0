<h1 align="center">🎲 Bingo Card Generator 2.0</h1>

<p align="center">
  Uma aplicação moderna e intuitiva para gerar cartelas de bingo personalizadas em PDF.
</p>

<p align="center">
  <img src="https://img.shields.io/github/license/Vectorgg15/BCG_2.0?style=flat-square" />
  <img src="https://img.shields.io/github/languages/top/Vectorgg15/BCG_2.0?style=flat-square" />
  <img src="https://img.shields.io/github/last-commit/Vectorgg15/BCG_2.0?style=flat-square" />
</p>

---

## 🧩 Funcionalidades

- 🧾 Geração automática de cartelas em formato PDF
- 🧠 Interface moderna com `CustomTkinter`
- 🎯 Suporte a modelos SVG e planilhas Excel
- 📤 Exportação em lote com barra de progresso
- ⛔ Cancelamento da geração com segurança

---

## 🖼️ Capturas de Tela

<p align="center">
  <img src="https://github.com/Vectorgg15/BCG_2.0/raw/main/Captura_de_tela_01.png" alt="Interface principal" width="700"/>
</p>

---

## 🚀 Instalação e Uso

### 1. Requisitos
- Python 3.8+
- Bibliotecas: `customtkinter`, `pandas`, `cairosvg`, `PyPDF2`, `Pillow`

### 2. Instalação
Primeiro, clone o repositório para a sua máquina. Depois, navegue até a pasta do projeto e instale todas as dependências com um único comando:

```bash
pip install -r requirements.txt
```

### 3. Execução
Para iniciar o programa, execute o seguinte comando no seu terminal:
```bash
python gerador_cartela_2.0.py
```

---

## 📄 Arquivos e Formato

Para gerar as cartelas, você precisará de dois arquivos: uma **Planilha Excel** com os dados e um **Modelo SVG** para o design.

### Planilha Excel (.xlsx)
A planilha deve conter os dados de cada cartela. É obrigatório que exista uma coluna chamada `N` para o número da cartela. Os nomes das outras colunas (ex: `B1`, `I1`, `N1`...) serão usados para substituir os textos correspondentes no modelo SVG.

**Exemplo:**
| N   | B1 | B2 | I1 | I2 | ... |
| --- | -- | -- | -- | -- | --- |
| 1   | 5  | 12 | 16 | 22 | ... |
| 2   | 3  | 15 | 28 | 17 | ... |


### Modelo SVG (.svg)
Este arquivo é o template visual da sua cartela.

#### **Como criar o seu modelo a partir do CorelDRAW:**
[cite_start]Conforme solicitado, você pode usar o arquivo `cartela bingo 2.0.cdr` [cite: 1] que está no projeto:
1. Abra o arquivo `cartela bingo 2.0.cdr` no CorelDRAW.
2. Edite **apenas os detalhes visuais** da cartela (cores, fontes, imagens de fundo, etc.).
3. **Não altere** os campos de texto que contêm os números (ex: `{{B1}}`, `{{N}}`), pois eles são os marcadores que o programa usa para gerar as cartelas.
4. Após finalizar o design, vá em `Arquivo > Exportar` e salve o arquivo com o formato **SVG**.

Este arquivo SVG exportado será o seu modelo para usar no programa.
