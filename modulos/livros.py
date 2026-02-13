import sqlite3
from database.conexao import criar_conexao

def cadastrarLivros():
    print('-=' * 30)
    print('     CADASTRO DE LIVROS')
    print('-=' * 30)

    titulo = str(input('Digite o título do livro: ')) # Use titulo em vez de nome
    autor = str(input('Digite o nome do autor: '))
    genero = str(input('Digite o gênero do livro: '))

    conn = criar_conexao()
    if conn:
        cursor = conn.cursor()
        try:
            sql = '''INSERT INTO livros (titulo, autor, genero) VALUES (?, ?, ?)'''
            cursor.execute(sql, (titulo, autor, genero))
            conn.commit()
            print(f"\n✅ Livro '{titulo}' adicionado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao inserir no banco: {e}")
        finally:
            conn.close()


def listarLivro():
    print("\n" + "="*30)
    print("  INVENTÁRIO DE LIVROS")
    print("="*30)
    
    conn = criar_conexao()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM livros")
        itens = cursor.fetchall()
        
        if not itens:
            print("Nenhum livro cadastrado até o momento.")
        else:
            for i in itens:
               print(f"ID: {i[0]} | Livro: {i[1]} | Autor: {i[2]} | Gênero: {i[3]}")
               
        input('Digite enter para voltar ao menu...')
        
        conn.close()

    
def buscar_livro():

    nome_busca = input("Digite o nome do livro para buscar: ")

    conn = criar_conexao() # Abre o túnel
    cursor = conn.cursor() # Chama o motorista
        
    # O '?' evita ataques de SQL Injection (segurança!)
    cursor.execute("SELECT * FROM livros WHERE titulo LIKE ?", (f'%{nome_busca}%',))
        
    resultados = cursor.fetchall() # Traz todos os encontrados
        
    if resultados:
        for item in resultados:
            print(f"ID: {item[0]} | Título: {item[1]} | Autor: {item[2]} | Gênero: {item[3]}")
        else:
            print("Nenhum livro encontrado.")
            
        input("\nPressione Enter para voltar ao menu...")
        
        conn.close()


def remover_livro():
    try:
        conn = criar_conexao()
        cursor = conn.cursor()

        # 1. Primeiro, mostramos o que existe no banco
        cursor.execute("SELECT id, titulo, autor FROM livros")
        livros = cursor.fetchall()

        if not livros:
            print("\n⚠️ Não há livros cadastrados para remover.")
            input("\nPressione Enter para voltar...")
            return # Sai da função se não houver nada

        print("\n" + "="*40)
        print("       LISTA DE LIVROS PARA REMOÇÃO")
        print("="*40)
        for livro in livros:
            print(f"ID: {livro[0]} | Título: {livro[1]} | Autor: {livro[2]}")
        print("="*40)

        # 2. Agora o usuário escolhe com base no que está vendo
        id_remover = int(input("\nDigite o ID do livro que deseja EXCLUIR (ou 0 para cancelar): "))

        if id_remover == 0:
            print("Operação cancelada.")
        else:
            # 3. Executa a remoção
            cursor.execute("DELETE FROM livros WHERE id = ?", (id_remover,))
            conn.commit()
            
            if cursor.rowcount > 0:
                print(f"\n✅ Livro com ID {id_remover} removido com sucesso!")
            else:
                print(f"\n⚠️ Nenhum livro encontrado com o ID {id_remover}.")

        input("\nPressione Enter para continuar...")

    except ValueError:
        print("\n⚠️ Erro: Por favor, digite um número de ID válido.")
        input("\nPressione Enter para tentar novamente...")
    except sqlite3.Error as e:
        print(f"\n❌ Erro no banco de dados: {e}")
    finally:
        if conn:
            conn.close()
    