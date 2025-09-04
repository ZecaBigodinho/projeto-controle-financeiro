import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd

load_dotenv()

def conectar():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT'),
            sslmode=os.getenv('DB_SSLMODE')
        )
        return conn
    except psycopg2.Error as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")
        return None

# --- Funções CRUD ---

def cadastrar_conta(nome, saldo_inicial):
    conn = conectar()
    if conn:
        try:
            cur = conn.cursor()
            sql = "INSERT INTO Contas (nome, saldo_inicial) VALUES (%s, %s)"
            cur.execute(sql, (nome, saldo_inicial))
            conn.commit()
            cur.close()
        except psycopg2.Error as e:
            print(f"Erro ao cadastrar conta: {e}")
        finally:
            conn.close()

def listar_contas():
    conn = conectar()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT conta_id, nome, saldo_inicial FROM Contas ORDER BY nome")
            contas = cur.fetchall()
            cur.close()
            return contas
        except psycopg2.Error as e:
            print(f"Erro ao listar contas: {e}")
            return []
        finally:
            conn.close()

def cadastrar_categoria(nome, tipo):
    conn = conectar()
    if conn:
        try:
            cur = conn.cursor()
            sql = "INSERT INTO Categorias (nome, tipo) VALUES (%s, %s)"
            cur.execute(sql, (nome, tipo))
            conn.commit()
            cur.close()
        except psycopg2.Error as e:
            print(f"Erro ao cadastrar categoria: {e}")
        finally:
            conn.close()

def listar_categorias():
    conn = conectar()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT categoria_id, nome, tipo FROM Categorias ORDER BY nome")
            categorias = cur.fetchall()
            cur.close()
            return categorias
        except psycopg2.Error as e:
            print(f"Erro ao listar categorias: {e}")
            return []
        finally:
            conn.close()

def deletar_categoria(categoria_id):
    
    conn = conectar()
    if conn:
        try:
            cur = conn.cursor()
            sql = "DELETE FROM Categorias WHERE categoria_id = %s"
            cur.execute(sql, (categoria_id,))
            conn.commit()
            cur.close()
            return True, "Categoria removida com sucesso!"
        except psycopg2.Error as e:
            # Erro específico para quando a categoria está em uso
            if hasattr(e, 'pgcode') and e.pgcode == '23503': # Código de erro para violação de chave estrangeira
                return False, "Erro: Categoria está em uso por transações e não pode ser removida."
            return False, f"Erro ao remover categoria: {e}"
        finally:
            conn.close()

def cadastrar_tag(nome):
    conn = conectar()
    if conn:
        try:
            cur = conn.cursor()
            sql = "INSERT INTO Tags (nome) VALUES (%s)"
            cur.execute(sql, (nome,))
            conn.commit()
            cur.close()
        except psycopg2.Error as e:
            print(f"Erro ao cadastrar tag: {e}")
        finally:
            conn.close()

def listar_tags():
    conn = conectar()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT tag_id, nome FROM Tags ORDER BY nome")
            tags = cur.fetchall()
            cur.close()
            return tags
        except psycopg2.Error as e:
            print(f"Erro ao listar tags: {e}")
            return []
        finally:
            conn.close()

def deletar_tag(tag_id):
    
    conn = conectar()
    if conn:
        try:
            cur = conn.cursor()
            sql = "DELETE FROM Tags WHERE tag_id = %s"
            cur.execute(sql, (tag_id,))
            conn.commit()
            cur.close()
            return True, "Tag removida com sucesso!"
        except psycopg2.Error as e:
            if hasattr(e, 'pgcode') and e.pgcode == '23503':
                return False, "Erro: Tag está em uso por transações e não pode ser removida."
            return False, f"Erro ao remover tag: {e}"
        finally:
            conn.close()

def cadastrar_transacao(descricao, valor, data, conta_id, categoria_id):

    conn = conectar()
    new_id = None
    if conn:
        try:
            cur = conn.cursor()
            sql = "INSERT INTO Transacoes (descricao, valor, data, conta_id, categoria_id) VALUES (%s, %s, %s, %s, %s) RETURNING transacao_id"
            cur.execute(sql, (descricao, valor, data, conta_id, categoria_id))
            new_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
        except psycopg2.Error as e:
            print(f"Erro ao cadastrar transação: {e}")
        finally:
            conn.close()
    return new_id

def associar_tag_transacao(transacao_id, tag_id):

    conn = conectar()
    if conn:
        try:
            cur = conn.cursor()
            sql = "INSERT INTO Transacao_Tag (transacao_id, tag_id) VALUES (%s, %s) ON CONFLICT DO NOTHING"
            cur.execute(sql, (transacao_id, tag_id))
            conn.commit()
            cur.close()
        except psycopg2.Error as e:
            print(f"Erro ao associar tag: {e}")
        finally:
            conn.close()

def listar_transacoes(filtro_conta_id=None, filtro_categoria_id=None):

    conn = conectar()
    if conn:
        try:
            cur = conn.cursor()
            sql = """
                SELECT t.transacao_id, t.descricao, t.valor, t.data, c.nome, cat.nome
                FROM Transacoes t
                JOIN Contas c ON t.conta_id = c.conta_id
                JOIN Categorias cat ON t.categoria_id = cat.categoria_id
            """
            params = []
            where_clauses = []
            if filtro_conta_id:
                where_clauses.append("t.conta_id = %s")
                params.append(filtro_conta_id)
            if filtro_categoria_id:
                where_clauses.append("t.categoria_id = %s")
                params.append(filtro_categoria_id)
            if where_clauses:
                sql += " WHERE " + " AND ".join(where_clauses)
            sql += " ORDER BY t.data DESC"
            cur.execute(sql, tuple(params))
            transacoes = cur.fetchall()
            cur.close()
            return transacoes
        except psycopg2.Error as e:
            print(f"Erro ao listar transações: {e}")
            return []
        finally:
            conn.close()

def importar_transacoes_excel(df):
    conn = conectar()
    if conn:
        sucessos = 0
        falhas = 0
        cur = conn.cursor()
        cur.execute("SELECT nome, conta_id FROM Contas")
        mapa_contas = {nome: cid for nome, cid in cur.fetchall()}
        cur.execute("SELECT nome, categoria_id FROM Categorias")
        mapa_categorias = {nome: cid for nome, cid in cur.fetchall()}
        for index, row in df.iterrows():
            try:
                conta_id = mapa_contas.get(row['conta_nome'])
                categoria_id = mapa_categorias.get(row['categoria_nome'])
                if conta_id is None or categoria_id is None:
                    falhas += 1
                    continue
                sql = "INSERT INTO Transacoes (descricao, valor, data, conta_id, categoria_id) VALUES (%s, %s, %s, %s, %s)"
                cur.execute(sql, (row['descricao'], row['valor'], row['data'], conta_id, categoria_id))
                sucessos += 1
            except Exception as e:
                print(f"Erro na linha {index}: {e}")
                falhas += 1
        conn.commit()
        cur.close()
        conn.close()
        return sucessos, falhas
    return 0, len(df)


# --- Funções de Agregação e Cálculo (Dashboard) ---

def calcular_saldo_total():
    conn = conectar()
    if conn:
        try:
            cur = conn.cursor()
            sql = """
                SELECT 
                    COALESCE((SELECT SUM(valor) FROM Transacoes WHERE categoria_id IN (SELECT categoria_id FROM Categorias WHERE tipo = 'Receita')), 0) -
                    COALESCE((SELECT SUM(valor) FROM Transacoes WHERE categoria_id IN (SELECT categoria_id FROM Categorias WHERE tipo = 'Despesa')), 0)
            """
            cur.execute(sql)
            saldo = cur.fetchone()[0]
            cur.close()
            return saldo if saldo is not None else 0.00
        except psycopg2.Error as e:
            print(f"Erro ao calcular saldo: {e}")
            return 0.00
        finally:
            conn.close()

def calcular_receitas_mes():
    conn = conectar()
    if conn:
        try:
            cur = conn.cursor()
            mes_atual = datetime.now().month
            ano_atual = datetime.now().year
            sql = """
                SELECT COALESCE(SUM(t.valor), 0.00)
                FROM Transacoes t
                JOIN Categorias cat ON t.categoria_id = cat.categoria_id
                WHERE cat.tipo = 'Receita'
                AND EXTRACT(MONTH FROM t.data) = %s
                AND EXTRACT(YEAR FROM t.data) = %s;
            """
            cur.execute(sql, (mes_atual, ano_atual))
            total = cur.fetchone()[0]
            cur.close()
            return total
        except psycopg2.Error as e:
            print(f"Erro ao calcular receitas do mês: {e}")
            return 0.00
        finally:
            conn.close()

def calcular_despesas_mes():
    conn = conectar()
    if conn:
        try:
            cur = conn.cursor()
            mes_atual = datetime.now().month
            ano_atual = datetime.now().year
            sql = """
                SELECT COALESCE(SUM(t.valor), 0.00)
                FROM Transacoes t
                JOIN Categorias cat ON t.categoria_id = cat.categoria_id
                WHERE cat.tipo = 'Despesa'
                AND EXTRACT(MONTH FROM t.data) = %s
                AND EXTRACT(YEAR FROM t.data) = %s;
            """
            cur.execute(sql, (mes_atual, ano_atual))
            total = cur.fetchone()[0]
            cur.close()
            return total
        except psycopg2.Error as e:
            print(f"Erro ao calcular despesas do mês: {e}")
            return 0.00
        finally:
            conn.close()

def get_gastos_por_categoria():
    conn = conectar()
    if conn:
        try:
            cur = conn.cursor()
            sql = """
                SELECT cat.nome, SUM(t.valor) as total
                FROM Transacoes t
                JOIN Categorias cat ON t.categoria_id = cat.categoria_id
                WHERE cat.tipo = 'Despesa'
                GROUP BY cat.nome
                ORDER BY total DESC;
            """
            cur.execute(sql)
            dados = cur.fetchall()
            cur.close()
            return dados
        except psycopg2.Error as e:
            print(f"Erro ao buscar gastos por categoria: {e}")
            return []
        finally:
            conn.close()