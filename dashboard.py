import streamlit as st
import pandas as pd
import database
from datetime import datetime
import plotly.express as px

# --- Configuração da Página ---
st.set_page_config(layout="wide", page_title="Dashboard Financeiro")

# --- INJEÇÃO DE CSS CUSTOMIZADO ---
st.markdown("""
<style>
    /* Fundo principal da aplicação */
    [data-testid="stAppViewContainer"] {
        background-color: #0F1116;
        color: #F0F2F6;
    }
    /* Fundo da barra lateral */
    [data-testid="stSidebar"] {
        background-color: #1C1E26;
    }
    /* Estilo dos títulos e cabeçalhos */
    h1, h2, h3 {
        color: #C5C6C7;
    }
    /* Estilo dos cards de métrica */
    [data-testid="stMetric"] {
        background-color: #2A2D3A;
        border: 1px solid #4A4E69;
        border-radius: 10px;
        padding: 15px;
    }
    /* Cor do valor da métrica */
    [data-testid="stMetricValue"] {
        color: #61A5C2;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL (SIDEBAR) ---

# Seção de Filtros
st.sidebar.header('Filtros 🔎')
contas_raw_filtro = database.listar_contas()
lista_contas_filtro = {conta[1]: conta[0] for conta in contas_raw_filtro}
lista_contas_filtro['Todas'] = None
conta_selecionada_filtro_nome = st.sidebar.selectbox('Filtrar por Conta', options=list(lista_contas_filtro.keys()))
filtro_conta_id_ativo = lista_contas_filtro[conta_selecionada_filtro_nome]

categorias_raw_filtro = database.listar_categorias()
lista_categorias_filtro = {cat[1]: cat[0] for cat in categorias_raw_filtro}
lista_categorias_filtro['Todas'] = None
categoria_selecionada_filtro_nome = st.sidebar.selectbox('Filtrar por Categoria', options=list(lista_categorias_filtro.keys()))
filtro_categoria_id_ativo = lista_categorias_filtro[categoria_selecionada_filtro_nome]

st.sidebar.markdown("---")

# Seção para Adicionar Transação
st.sidebar.header('Adicionar Nova Transação ✍️')
with st.sidebar.form("nova_transacao_form", clear_on_submit=True):
    descricao_transacao = st.text_input('Descrição')
    valor_transacao = st.number_input('Valor', min_value=0.0, format="%.2f")
    data_transacao = st.date_input('Data', datetime.now().date())
    contas_raw = database.listar_contas()
    lista_contas_nomes = {conta[1]: conta[0] for conta in contas_raw}
    conta_selecionada_nome = st.selectbox('Conta', options=list(lista_contas_nomes.keys()))
    categorias_raw = database.listar_categorias()
    lista_categorias_nomes = {cat[1]: cat[0] for cat in categorias_raw}
    categoria_selecionada_nome = st.selectbox('Categoria', options=list(lista_categorias_nomes.keys()))
    tags_raw = database.listar_tags()
    lista_tags_nomes = {tag[1]: tag[0] for tag in tags_raw}
    tags_selecionadas_nomes = st.multiselect('Tags (Opcional)', options=list(lista_tags_nomes.keys()))
    submitted = st.form_submit_button("Adicionar Transação")
    if submitted:
        if descricao_transacao and valor_transacao > 0:
            conta_id = lista_contas_nomes[conta_selecionada_nome]
            categoria_id = lista_categorias_nomes[categoria_selecionada_nome]
            nova_transacao_id = database.cadastrar_transacao(
                descricao_transacao, valor_transacao, data_transacao, conta_id, categoria_id
            )
            if nova_transacao_id and tags_selecionadas_nomes:
                for nome_tag in tags_selecionadas_nomes:
                    tag_id = lista_tags_nomes[nome_tag]
                    database.associar_tag_transacao(nova_transacao_id, tag_id)
            st.sidebar.success('Transação adicionada com sucesso!')
            st.rerun()
        else:
            st.sidebar.error('Por favor, preencha todos os campos obrigatórios.')

st.sidebar.markdown("---")

# --- SEÇÃO ATUALIZADA: GERENCIAR ITENS ---
st.sidebar.header('Gerenciar Itens 🛠️')

with st.sidebar.expander("Contas", expanded=False):
    # Expander para visualizar as contas existentes
    with st.expander("Visualizar Contas Cadastradas"):
        contas = database.listar_contas()
        if contas:
            for conta in contas:
                st.write(f"- {conta[1]} (Saldo: R$ {conta[2]:.2f})")
        else:
            st.info("Nenhuma conta cadastrada.")
    
    # Formulário para cadastrar uma nova conta
    with st.form("nova_conta_form", clear_on_submit=True):
        nome_conta = st.text_input("Nome da Nova Conta")
        saldo_conta = st.number_input("Saldo Inicial", min_value=0.0, format="%.2f")
        if st.form_submit_button("Cadastrar Conta"):
            if nome_conta:
                database.cadastrar_conta(nome_conta, saldo_conta)
                st.success(f"Conta '{nome_conta}' cadastrada!")
                st.rerun()
            else:
                st.error("O nome da conta não pode estar vazio.")

with st.sidebar.expander("Categorias"):
    # Formulário para cadastrar
    with st.form("nova_categoria_form", clear_on_submit=True):
        st.write("**Cadastrar Nova Categoria**")
        nome_categoria = st.text_input("Nome da Nova Categoria")
        tipo_categoria = st.selectbox("Tipo", ["Receita", "Despesa"])
        if st.form_submit_button("Cadastrar"):
            if nome_categoria:
                database.cadastrar_categoria(nome_categoria, tipo_categoria)
                st.success(f"Categoria '{nome_categoria}' cadastrada!")
                st.rerun()
    st.markdown("---")
    # Formulário para remover
    with st.form("remover_categoria_form", clear_on_submit=True):
        st.write("**Remover Categoria Existente**")
        categorias_raw = database.listar_categorias()
        lista_categorias_nomes = {cat[1]: cat[0] for cat in categorias_raw}
        categoria_para_remover = st.selectbox("Selecione a Categoria para Remover", options=list(lista_categorias_nomes.keys()))
        if st.form_submit_button("Remover"):
            categoria_id = lista_categorias_nomes.get(categoria_para_remover)
            if categoria_id:
                sucesso, mensagem = database.deletar_categoria(categoria_id)
                if sucesso:
                    st.success(mensagem)
                    st.rerun()
                else:
                    st.error(mensagem)

with st.sidebar.expander("Tags"):
    # Formulário para cadastrar
    with st.form("nova_tag_form", clear_on_submit=True):
        st.write("**Cadastrar Nova Tag**")
        nome_tag = st.text_input("Nome da Nova Tag (ex: emergência)")
        if st.form_submit_button("Cadastrar"):
            if nome_tag:
                database.cadastrar_tag(nome_tag)
                st.success(f"Tag '{nome_tag}' cadastrada!")
                st.rerun()
    st.markdown("---")
    # Formulário para remover
    with st.form("remover_tag_form", clear_on_submit=True):
        st.write("**Remover Tag Existente**")
        tags_raw = database.listar_tags()
        lista_tags_nomes = {tag[1]: tag[0] for tag in tags_raw}
        tag_para_remover = st.selectbox("Selecione a Tag para Remover", options=list(lista_tags_nomes.keys()))
        if st.form_submit_button("Remover"):
            tag_id = lista_tags_nomes.get(tag_para_remover)
            if tag_id:
                sucesso, mensagem = database.deletar_tag(tag_id)
                if sucesso:
                    st.success(mensagem)
                    st.rerun()
                else:
                    st.error(mensagem)

st.sidebar.markdown("---")

# Seção para Importar do Excel
st.sidebar.header('Importar Dados 📤')
uploaded_file = st.sidebar.file_uploader("Escolha um arquivo Excel (.xlsx)", type="xlsx")
if uploaded_file is not None:
    try:
        df_excel = pd.read_excel(uploaded_file)
        colunas_necessarias = ['descricao', 'valor', 'data', 'conta_nome', 'categoria_nome']
        if not all(col in df_excel.columns for col in df_excel.columns):
            st.sidebar.error(f"O arquivo Excel precisa conter as colunas: {', '.join(colunas_necessarias)}")
        else:
            st.sidebar.write("Pré-visualização dos dados:")
            st.sidebar.dataframe(df_excel.head())
            if st.sidebar.button("Confirmar Importação"):
                sucesso, falha = database.importar_transacoes_excel(df_excel)
                st.sidebar.success(f"{sucesso} transações importadas!")
                if falha > 0:
                    st.sidebar.warning(f"{falha} transações falharam (verifique se as contas e categorias existem).")
                st.rerun()
    except Exception as e:
        st.sidebar.error(f"Erro ao ler o arquivo: {e}")

# --- PÁGINA PRINCIPAL ---

st.title('Meu Dashboard Financeiro 📊')

# --- Seção de Métricas Principais ---
st.header('Visão Geral')
saldo_total = database.calcular_saldo_total()
receitas_mes = database.calcular_receitas_mes()
despesas_mes = database.calcular_despesas_mes()
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Saldo Total", value=f"R$ {saldo_total:.2f}")
with col2:
    st.metric(label="Receitas do Mês", value=f"R$ {receitas_mes:.2f}")
with col3:
    st.metric(label="Despesas do Mês", value=f"R$ {despesas_mes:.2f}")

st.markdown("---")

# --- Histórico de Transações (Tabela Principal) ---
st.header('Histórico de Transações Recentes 🧾')
transacoes = database.listar_transacoes(filtro_conta_id=filtro_conta_id_ativo, filtro_categoria_id=filtro_categoria_id_ativo)
if transacoes:
    df_transacoes = pd.DataFrame(transacoes, columns=['ID', 'Descrição', 'Valor', 'Data', 'Conta', 'Categoria'])
    st.dataframe(df_transacoes)
else:
    st.info('Nenhuma transação encontrada para os filtros selecionados.')

st.markdown("---")

# --- Seção de Gráfico ---
st.header('Análise de Despesas 📈')
gastos_categoria = database.get_gastos_por_categoria()
if gastos_categoria:
    df_gastos = pd.DataFrame(gastos_categoria, columns=['Categoria', 'Total Gasto'])
    fig = px.pie(
        df_gastos, 
        names='Categoria', 
        values='Total Gasto', 
        title='Distribuição de Gastos por Categoria',
        color_discrete_sequence=px.colors.sequential.Plasma
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Não há dados de despesas para exibir no gráfico.")