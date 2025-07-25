# Gerador de Cartelas de Bingo 2.0

![Captura de Tela](https://github.com/Vectorgg15/BCG_2.0/raw/main/Captura_de_tela_01.png)

Uma aplicação de desktop moderna e intuitiva para gerar cartelas de bingo personalizadas em formato PDF a partir de dados de uma planilha Excel e um modelo SVG.

---

## ✨ Funcionalidades

- **Interface Gráfica Intuitiva:** Desenvolvido com CustomTkinter para uma experiência de usuário agradável.
- **Geração a partir de Planilhas:** Carregue os dados das cartelas diretamente de um arquivo `.xlsx`.
- **Templates Personalizáveis:** Use seus próprios modelos de cartela em formato `.svg` para total liberdade de design.
- **Geração em Lote:** Crie centenas de cartelas de uma vez, seja por um intervalo de números ou por uma lista específica.
- **Exportação para PDF:** Todas as cartelas são salvas em um único arquivo PDF, prontas para impressão.
- **Processamento Seguro:** A geração ocorre em uma thread separada para não travar a interface, com feedback de progresso e opção de cancelamento.

---

## 🚀 Instalação e Uso

### Pré-requisitos
- Python 3.8 ou superior

### Passos

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/Vectorgg15/BCG_2.0.git](https://github.com/Vectorgg15/BCG_2.0.git)
    cd BCG_2.0
    ```

2.  **Crie um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    ```
    - No Windows: `venv\Scripts\activate`
    - No Linux/macOS: `source venv/bin/activate`

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação:**
    ```bash
    python gerador_cartela_2.0.py
    ```

---

## 📝 Como Usar

1.  **Carregar Arquivos:**
    - Clique em "Procurar..." para selecionar sua **Planilha Excel** (`.xlsx`).
    - Clique em "Procurar..." para selecionar seu **Modelo SVG** (`.svg`).
    - Clique em **"Carregar Planilha"**.

2.  **Gerar Cartelas:**
    - **Por Intervalo:** Digite o número da cartela inicial e final e clique em "GERAR POR INTERVALO".
    - **Por Lista:** Digite os números das cartelas desejadas, separados por vírgula (ex: `5, 23, 112`), e clique em "GERAR CARTELAS ESPECÍFICAS".

3.  **Salvar o PDF:**
    - Uma janela de diálogo aparecerá para você escolher onde salvar o arquivo PDF gerado.

---

## 📄 Formato dos Arquivos

### Planilha Excel
A planilha deve conter uma coluna chamada `N` para o número de identificação da cartela. Os nomes das outras colunas serão usados como "placeholders" no SVG.

**Exemplo (`Exemplo_Cartelas.xlsx`):**
| N | B1 | B2 | I1 | I2 |
|---|---|---|---|---|
| 1 | 5 | 12 | 16 | 22 |
| 2 | 3 | 15 | 28 | 17 |

### Modelo SVG
O arquivo SVG deve conter "placeholders" no formato `{{NOME_DA_COLUNA}}` onde os dados da planilha serão inseridos.

**Exemplo (`Modelo_Cartela.svg`):**
```xml
<text x="20" y="60">Cartela Nº: {{N}}</text>
<text x="40" y="100">{{B1}}</text>
<text x="100" y="100">{{I1}}</text>
```

---

## 📜 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).
