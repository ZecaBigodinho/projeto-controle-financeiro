-- Tabela para armazenar as contas (ex: Carteira, Banco, Cartão de Crédito)
CREATE TABLE Contas (
    conta_id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    saldo_inicial NUMERIC(10, 2) NOT NULL DEFAULT 0.00
);

-- Tabela para classificar as transações
CREATE TABLE Categorias (
    categoria_id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    tipo VARCHAR(7) NOT NULL CHECK (tipo IN ('Receita', 'Despesa'))
);

-- Tabela principal que registra cada transação
CREATE TABLE Transacoes (
    transacao_id SERIAL PRIMARY KEY,
    descricao VARCHAR(255) NOT NULL,
    valor NUMERIC(10, 2) NOT NULL,
    data DATE NOT NULL DEFAULT CURRENT_DATE,
    
    -- Chaves Estrangeiras
    conta_id INT NOT NULL,
    categoria_id INT NOT NULL,
    
    FOREIGN KEY (conta_id) REFERENCES Contas(conta_id),
    FOREIGN KEY (categoria_id) REFERENCES Categorias(categoria_id)
);

-- Tabela para as tags (etiquetas)
CREATE TABLE Tags (
    tag_id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);

-- Tabela associativa para a relação N-para-N entre Transacoes e Tags
CREATE TABLE Transacao_Tag (
    transacao_id INT NOT NULL,
    tag_id INT NOT NULL,
    
    -- Chave primária composta para garantir que a mesma tag não seja adicionada duas vezes na mesma transação
    PRIMARY KEY (transacao_id, tag_id),
    
    FOREIGN KEY (transacao_id) REFERENCES Transacoes(transacao_id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES Tags(tag_id) ON DELETE CASCADE
);

-- Inserindo algumas categorias
INSERT INTO Categorias (nome, tipo) VALUES
('Salário', 'Receita'),
('Outras Receitas', 'Receita'),
('Alimentação', 'Despesa'),
('Transporte', 'Despesa'),
('Moradia', 'Despesa'),
('Lazer', 'Despesa'),
('Saúde', 'Despesa'),
('Educação', 'Despesa'),
('Outras Despesas', 'Despesa');