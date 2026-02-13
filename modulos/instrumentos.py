from database.conexao import criar_conexao
import sqlite3

def cadastrar_instrumento():

    try:
        # Seguindo as especificações exatas da dona
        tipo = input("Tipo: ")
        marca = input("Marca: ")
        modelo = input("Modelo: ")
        numero = input("Número (Série/Patrimônio): ")
        origem = input("Origem: ")
        aluno_responsavel = input("Responsável: ")
        contato_aluno = input("Telefone (Fixo/Celular): ")

        conn = criar_conexao()
        cursor = conn.cursor()
        
        sql = '''INSERT INTO instrumentos
(tipo, marca, modelo, numero, origem, aluno_responsavel, contato_aluno)
VALUES (?, ?, ?, ?, ?, ?, ?)'''
        
        cursor.execute(sql, (tipo, marca, modelo, numero, origem, aluno_responsavel, contato_aluno))
        conn.commit()
        print(f"\n✅ Instrumento '{tipo} - {marca}' adicionado com sucesso!")
        
    except sqlite3.Error as e:
        print(f"❌ Erro ao salvar no banco: {e}")
    finally:
        if conn: conn.close()
    
    input("\nPressione Enter para continuar...")


def listar_instrumentos():
    print("\n" + "="*60)
    print(f"{'ID':<4} | {'TIPO/MARCA':<20} | {'ALUNO RESPONSÁVEL':<20} | {'CONTATO'}")
    print("-" * 60)
    
    conn = criar_conexao()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, tipo, marca, aluno_responsavel, contato_aluno FROM instrumentos")
        itens = cursor.fetchall()
        
        if not itens:
            print("Nenhum instrumento cadastrado.")
        else:
            for i in itens:
                # Formatando a exibição em colunas para facilitar a leitura
                tipo_marca = f"{i[1]} {i[2]}"
                aluno = i[3] if i[3] else "Na Biblioteca"
                contato = i[4] if i[4] else "N/A"
                print(f"{i[0]:<4} | {tipo_marca[:20]:<20} | {aluno[:20]:<20} | {contato}")
        
        conn.close()
    input("\nPressione Enter para continuar...")


def buscar_instrumento():
    termo = input("Digite o nome ou tipo para buscar: ").strip().lower()
    
    conn = criar_conexao()
    cursor = conn.cursor()
    
    # O LOWER(tipo) faz o banco ignorar se é maiúsculo ou minúsculo
    sql = "SELECT * FROM instrumentos WHERE LOWER(tipo) LIKE ? OR LOWER(aluno_responsavel) LIKE ?"
    cursor.execute(sql, (f'%{termo}%', f'%{termo}%'))
        
    resultados = cursor.fetchall() # Traz todos os encontrados
        
    if resultados:
        for item in resultados:
            print(f"ID: {item[0]} | Nome: {item[2]} | Origem: {item[3]}")
    else:
        print("Nenhum instrumento encontrado.")
        
    conn.close()
    input("\nPressione Enter para continuar...")


def atualizar_posse():
    listar_instrumentos()
    try:
        id_inst = int(input("\nDigite o ID do instrumento para atualizar a posse: "))
        novo_aluno = input("Nome do Aluno que está com o instrumento: ")
        novo_contato = input("Telefone de contato: ")
        
        conn = criar_conexao()
        cursor = conn.cursor()
        
        sql = "UPDATE instrumentos SET aluno_responsavel = ?, contato_aluno = ? WHERE id = ?"
        cursor.execute(sql, (novo_aluno, novo_contato, id_inst))
        conn.commit()
        
        if cursor.rowcount > 0:
            print(f"\n✅ Posse do instrumento {id_inst} atualizada para {novo_aluno}!")
        else:
            print("\n⚠️ ID não encontrado.")
            
    except ValueError:
        print("⚠️ Erro: Digite um número válido para o ID.")
    finally:
        if conn: conn.close()
    input("\nPressione Enter para continuar...")


def remover_instrumento():

    id_excluir = input("Digite o ID do instrumento que deseja remover: ")
    
    conn = criar_conexao()
    cursor = conn.cursor()
            
    cursor.execute("DELETE FROM instrumentos WHERE id = ?", (id_excluir,))
            
    conn.commit() # IMPORTANTE: Para Deletar/Inserir/Alterar
    conn.close()
    print("Remoção concluída.")


def pegar_todos_instrumentos():
    """Retorna uma lista de dicionários com todos os instrumentos para a Web."""
    conn = criar_conexao()
    # Configura o cursor para retornar dicionários em vez de tuplas
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM instrumentos")
    linhas = cursor.fetchall()
    conn.close()
    
    # Transforma o resultado em uma lista de dicionários comum
    return [dict(linha) for linha in linhas]