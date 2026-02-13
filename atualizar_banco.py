import sqlite3

# Nome do seu arquivo de banco de dados
BANCO = 'biblioteca_comunitaria.db'

def adicionar_coluna():
    try:
        conn = sqlite3.connect(BANCO)
        cursor = conn.cursor()
        
        # O comando que vai adicionar a coluna de data
        cursor.execute("ALTER TABLE instrumentos ADD COLUMN data_emprestimo TEXT;")
        
        conn.commit()
        print("✅ Sucesso! A coluna 'data_emprestimo' foi adicionada.")
    except sqlite3.OperationalError:
        print("⚠️ Aviso: A coluna já existe ou o banco não foi encontrado.")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    adicionar_coluna()