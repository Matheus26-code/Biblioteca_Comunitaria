from database.conexao import inicializar_banco
from modulos.instrumentos import *
from modulos.livros import *
import os

def limpar_tela():
    if os.name == 'nt':
        # Tenta limpar o terminal e o histórico do buffer
        os.system('cls')
        print("\033[H\033[J", end="")
    else:
        os.system('clear')


def escolhaMenu():
    
    print('''Escolha a opcao desejada
1 - GERENCIAMENTO DE LIVROS
2 - GERENCIAMENTO DE INTRUMENTOS''')
    

    opcao = int(input('Digite o gerenciador que gostaria de abrir: '))
    if opcao == 1:
        menuLivro()
    elif opcao == 2:
        menuInstrumento()


def menuLivro():
    #Inicia as tabelas no banco de dados para livros
    inicializar_banco()
    
    while True:
        limpar_tela()
        print("\n" + "="*30)
        print("  SISTEMA LIVROS")
        print("="*30)
        print('''
1 - Cadastrar Livros
2 - Buscar Livros
3 - Remover Livros
4 - Atualizar Livros
5 - Listar Livros
0 - Sair do menu
9 - Voltar ao menu anterior'''
)
        
        opcao = input("\nEscolha uma opção: ")
            
        if opcao == '1':
            cadastrarLivros()
        elif opcao == '2':
            buscar_livro()
        elif opcao ==  '3':
            remover_livro()
        elif opcao == '5':
            listarLivro()
        elif opcao == '9':
            escolhaMenu()
        elif opcao == '0':
            print('Saindo...')
            break
        else:
            print('Opção Inválida!')


def menuInstrumento():
     #Inicia as tabelas no banco de dados para instrumentos
     inicializar_banco()

     while True:
        limpar_tela()
        print("\n" + "="*30)
        print("    SISTEMA INSTRUMENTOS")
        print("="*30)
        print("1 - Cadastrar Instrumento")
        print("2 - Listar Instrumentos")
        print("3 - Buscar Instrumento")
        print("4 - Atualizar Posse")
        print("5 - Remover Instrumento")
        print("9 - Voltar ao menu anterior")
        print("0 - Sair")
        
        opcao = input("\nEscolha uma opção: ")
            
        if opcao == '1':
            cadastrar_instrumento()
        elif opcao == '2':
            listar_instrumentos()
        elif opcao == '3':
            buscar_instrumento()
        elif opcao == '4':
            atualizar_posse()
        elif opcao == '5':
            remover_instrumento()
        elif opcao == '9':
            escolhaMenu()
        elif opcao == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    escolhaMenu()