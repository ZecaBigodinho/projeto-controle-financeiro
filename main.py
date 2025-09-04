import database
from rich.console import Console
from rich.table import Table
from datetime import datetime
import subprocess
import webbrowser
import time

console = Console()
streamlit_process = None

# --- FUNÇÕES DE EXIBIÇÃO ---

def mostrar_contas():

    contas = database.listar_contas()
    tabela = Table(title="Minhas Contas")
    tabela.add_column("ID", style="cyan", justify="right")
    tabela.add_column("Nome", style="magenta")
    tabela.add_column("Saldo Inicial", justify="right", style="green")
    for conta in contas:
        tabela.add_row(str(conta[0]), conta[1], f"R$ {conta[2]:.2f}")
    console.print(tabela)

def mostrar_categorias():

    categorias = database.listar_categorias()
    tabela = Table(title="Categorias de Transações")
    tabela.add_column("ID", style="cyan", justify="right")
    tabela.add_column("Nome", style="magenta")
    tabela.add_column("Tipo", style="yellow")
    for categoria in categorias:
        tabela.add_row(str(categoria[0]), categoria[1], categoria[2])
    console.print(tabela)

def mostrar_tags():

    tags = database.listar_tags()
    tabela = Table(title="Tags")
    tabela.add_column("ID", style="cyan", justify="right")
    tabela.add_column("Nome", style="magenta")
    for tag in tags:
        tabela.add_row(str(tag[0]), tag[1])
    console.print(tabela)

def mostrar_transacoes():

    transacoes = database.listar_transacoes()
    tabela = Table(title="Histórico de Transações")
    tabela.add_column("ID", style="cyan", justify="right")
    tabela.add_column("Descrição", width=30)
    tabela.add_column("Valor", justify="right", style="green")
    tabela.add_column("Data", justify="center")
    tabela.add_column("Conta")
    tabela.add_column("Categoria", style="yellow")
    for transacao in transacoes:
        valor = f"R$ {transacao[2]:.2f}"
        data = transacao[3].strftime("%d/%m/%Y")
        tabela.add_row(str(transacao[0]), transacao[1], valor, data, transacao[4], transacao[5])
    console.print(tabela)

def abrir_dashboard_web():

    global streamlit_process
    if streamlit_process is None or streamlit_process.poll() is not None:
        console.print("[yellow]Iniciando o servidor do dashboard pela primeira vez... Aguarde.[/yellow]")
        command = ["python", "-m", "streamlit", "run", "dashboard.py", "--server.headless=true"]
        streamlit_process = subprocess.Popen(command)
        time.sleep(5)
        url = "http://localhost:8501"
        webbrowser.open(url)
        console.print(f"[bold green]Dashboard iniciado com sucesso! Acesse em: {url}[/bold green]")
    else:
        url = "http://localhost:8501"
        console.print(f"[cyan]O servidor do dashboard já está em execução. Acesse em: {url}[/cyan]")
        webbrowser.open(url)
    console.print("[italic]Para parar o servidor, feche esta janela do terminal principal.[/italic]")


# --- FUNÇÃO PRINCIPAL E MENU ATUALIZADO ---

def main():

    while True:
        saldo_total = database.calcular_saldo_total()
        console.print(f"\n[bold green]Saldo Total Geral: R$ {saldo_total:.2f}[/bold green]")
        
        console.print("\n[bold magenta]Painel de Controle Financeiro[/bold magenta]")
        console.print("[yellow]-- Transações --[/yellow]")
        console.print("1. Listar Transações")
        console.print("2. Adicionar Transação")
        console.print("3. Associar Tag a uma Transação")
        console.print("[yellow]-- Gerenciamento --[/yellow]")
        console.print("4. Listar Contas")
        console.print("5. Cadastrar Nova Conta")
        console.print("6. Listar Categorias")
        console.print("7. Cadastrar Nova Categoria")
        console.print("8. Listar Tags")
        console.print("9. Cadastrar Nova Tag")
        console.print("[yellow]-- Visualização --[/yellow]")
        console.print("10. ✨ Abrir Dashboard Web Interativo")
        console.print("[yellow]-- Sair --[/yellow]")
        console.print("0. Sair")
        
        opcao = input("Escolha uma opção: ")

        try:
            if opcao == '1':
                mostrar_transacoes()
            elif opcao == '2':
                console.print("\n--- [bold]Adicionar Nova Transação[/bold] ---")
                descricao = input("Descrição: ")
                valor = float(input("Valor: "))
                mostrar_contas()
                conta_id = int(input("ID da Conta de origem: "))
                mostrar_categorias()
                categoria_id = int(input("ID da Categoria: "))
                data = datetime.now().date()
                database.cadastrar_transacao(descricao, valor, data, conta_id, categoria_id)
            elif opcao == '3':
                console.print("\n--- [bold]Associar Tag a uma Transação[/bold] ---")
                mostrar_transacoes()
                transacao_id = int(input("ID da Transação: "))
                mostrar_tags()
                tag_id = int(input("ID da Tag a ser associada: "))
                database.associar_tag_transacao(transacao_id, tag_id)
            elif opcao == '4':
                mostrar_contas()
            elif opcao == '5':
                 console.print("\n--- [bold]Cadastrar Nova Conta[/bold] ---")
                 nome = input("Nome da nova conta: ")
                 saldo = float(input("Saldo inicial: "))
                 database.cadastrar_conta(nome, saldo)
            elif opcao == '6':
                mostrar_categorias()
            elif opcao == '7':
                console.print("\n--- [bold]Cadastrar Nova Categoria[/bold] ---")
                nome = input("Nome da nova categoria: ")
                tipo = input("Tipo ('Receita' ou 'Despesa'): ").capitalize()
                if tipo in ['Receita', 'Despesa']:
                    database.cadastrar_categoria(nome, tipo)
                else:
                    console.print("[bold red]Erro: Tipo deve ser 'Receita' ou 'Despesa'[/bold red]")
            elif opcao == '8':
                mostrar_tags()
            elif opcao == '9':
                console.print("\n--- [bold]Cadastrar Nova Tag[/bold] ---")
                nome = input("Nome da nova tag: ")
                database.cadastrar_tag(nome)
            elif opcao == '10':
                abrir_dashboard_web()
            elif opcao == '0':
                console.print("[bold cyan]Saindo... Até logo![/bold cyan]")
                break
            else:
                console.print("[bold red]Opção inválida! Tente novamente.[/bold red]")
        
        except ValueError:
            console.print("[bold red]Erro: Entrada inválida. Por favor, insira um número onde for solicitado.[/bold red]")
        except Exception as e:
            console.print(f"[bold red]Ocorreu um erro inesperado: {e}[/bold red]")

#play
if __name__ == "__main__":
    main()