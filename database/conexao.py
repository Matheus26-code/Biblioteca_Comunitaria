import sqlite3

def criar_conexao():
    """Estabelece a conexão com o banco de dados local."""
    try:
        conn = sqlite3.connect('biblioteca_comunitaria.db')
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco: {e}")
        return None


def inicializar_banco():
    """Cria as tabelas necessárias se elas não existirem."""
    conn = criar_conexao()
    if conn:
        cursor = conn.cursor()
        
        # Tabela de Livros
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                autor TEXT NOT NULL,
                genero TEXT,
                status_emprestimo TEXT DEFAULT 'Disponível'
            )
        ''')
        
    # Tabela de Instrumentos (Foco na necessidade da dona)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS instrumentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL,
        marca TEXT,
        modelo TEXT,
        numero TEXT,
        origem TEXT,
        aluno_responsavel TEXT, -- Nome do aluno que está com o instrumento
        contato_aluno TEXT,      -- Telefone do aluno
        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
        
    conn.commit()
    conn.close()
    print("Estrutura de dados inicializada com sucesso!")


if __name__ == "__main__":
    inicializar_banco()