import sqlite3

# Nome do seu arquivo de banco de dados
BANCO = 'biblioteca_comunitaria.db'

def adicionar_coluna():
    conn = sqlite3.connect(BANCO)
    cursor = conn.cursor()
    
    # Lista de novas colunas para adicionar
    novas_colunas = [
        "cidade TEXT", 
        "bairro TEXT", 
        "rua TEXT", 
        "numero_casa TEXT"
    ]

    for coluna in novas_colunas:
        try:
            # Tenta adicionar uma por uma
            cursor.execute(f"ALTER TABLE instrumentos ADD COLUMN {coluna}")
            print(f"✅ Coluna {coluna.split()[0]} adicionada com sucesso!")
        except sqlite3.OperationalError:
            # Se a coluna já existir, ele apenas pula para a próxima sem travar
            print(f"⚠️ Coluna {coluna.split()[0]} já existe, pulando...")

    conn.commit()
    conn.close()
    print("🚀 Processo de atualização concluído!")

if __name__ == "__main__":
    adicionar_coluna()