# 📊 Projeto de Controle Financeiro Pessoal

Projeto acadêmico desenvolvido para a disciplina de **Desenvolvimento com Banco de Dados**, consistindo em um sistema híbrido para gerenciamento de finanças pessoais.

O sistema possui uma interface de linha de comando (CLI) para operações rápidas e um dashboard web interativo e moderno para visualização e análise de dados.

## ✨ Funcionalidades Principais

- **CRUD Completo:** Gerenciamento total (Criar, Ler, Atualizar, Deletar) de Contas, Categorias e Tags.
- **Registro de Transações:** Cadastro detalhado de receitas e despesas.
- **Relacionamento N:N:** Associação de múltiplas Tags a uma única Transação para uma categorização flexível.
- **Interface Híbrida:**
    - **CLI (Terminal):** Interface rápida e eficiente para todas as operações de dados.
    - **Dashboard Web:** Interface visual construída com Streamlit para uma experiência de usuário rica e intuitiva.
- **Análise de Dados:**
    - Métricas em tempo real (Saldo Total, Receitas/Despesas do Mês).
    - Gráfico interativo de pizza para análise da distribuição de despesas.
    - Filtros dinâmicos na tabela de transações por Conta e Categoria.
- **Importação de Dados:** Funcionalidade para importar transações em massa a partir de um arquivo Excel (.xlsx).

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3
- **Banco de Dados:** PostgreSQL
- **Bibliotecas Python:**
    - `psycopg2-binary` (Conexão com PostgreSQL)
    - `streamlit` (Dashboard Web)
    - `pandas` (Manipulação de dados e importação de Excel)
    - `plotly` (Gráficos interativos)
    - `rich` (Interface de terminal rica)
    - `python-dotenv` (Gerenciamento de variáveis de ambiente)

## ⚙️ Estrutura do Projeto

- `main.py`: Ponto de entrada para a aplicação de terminal (CLI).
- `dashboard.py`: Ponto de entrada para o dashboard web (Streamlit).
- `database.py`: Módulo central que contém toda a lógica de interação com o banco de dados.
- `schema.sql`: Script para criação de todas as tabelas e restrições no PostgreSQL.
- `requirements.txt`: Lista de dependências Python para fácil instalação do ambiente.

## 🚀 Como Executar o Projeto

Siga os passos abaixo para configurar e rodar a aplicação em um ambiente local.

### **1. Pré-requisitos**

- Python 3.8 ou superior.
- PostgreSQL instalado e um servidor em execução.
- Git.

### **2. Configuração do Ambiente**

```bash
# 1. Clone o repositório
git clone [COLE A URL DO SEU REPOSITÓRIO AQUI]
cd [NOME_DA_PASTA_DO_REPOSITORIO]

# 2. (Recomendado) Crie e ative um ambiente virtual
python -m venv venv
# No Windows:
.\venv\Scripts\activate
# No macOS/Linux:
# source venv/bin/activate

# 3. Instale as dependências do projeto
pip install -r requirements.txt
```

### **3. Configuração do Banco de Dados**

1. Crie um novo banco de dados no seu PostgreSQL (ex: `financas_db`).
2. Execute o script `schema.sql` neste banco de dados para criar todas as tabelas e inserir as categorias padrão. Você pode fazer isso usando o pgAdmin, DBeaver ou outra ferramenta de sua preferência.

### **4. Configuração das Variáveis de Ambiente**

1.  Renomeie o arquivo `.env.example` para `.env`.
2.  Abra o arquivo `.env` e preencha com as suas credenciais de conexão ao PostgreSQL (usuário, senha, host, porta e o nome do banco que você criou no passo anterior).

### **5. Execução da Aplicação**

Você pode rodar a aplicação de duas formas:

- **Para usar a interface de terminal (CLI):**
  ```bash
  python main.py
  ```

- **Para usar o dashboard web interativo:**
  ```bash
  python -m streamlit run dashboard.py
  ```
  O dashboard será aberto automaticamente no seu navegador.

## 🏛️ Schema do Banco de Dados (DER)

A estrutura do banco de dados está definida no arquivo `schema.sql`.
## 👨‍💻 Autor

- **Pedro Paulo Izaias Félix**

OBS: O TAL DO RAPHAEL É APENAS O USUÁRIO QUE TAVA SALVO NA DROGA DO VSCODE, NÃO SEI COMO REMOVER ;-;
