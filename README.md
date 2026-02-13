# 📚 Sistema de Inventário - Biblioteca Comunitária

Este projeto foi desenvolvido como parte do **Projeto de Extensão** do curso de **Análise e Desenvolvimento de Sistemas (Anhanguera)**. O objetivo é fornecer uma ferramenta simples e segura para a gestão de livros e instrumentos musicais de uma biblioteca comunitária local.

## 🚀 Funcionalidades

* **Autenticação Segura**: Sistema de login para proteger os dados de acesso restrito.
* **Gestão de Inventário**: Cadastro, edição, visualização e exclusão de itens (CRUD).
* **Controle de Cautela**: Registro automático de quem está com o instrumento e desde quando.
* **Busca Dinâmica**: Filtro rápido para localizar itens no banco de dados.
* **Banco de Dados Local**: Utiliza SQLite para facilitar a portabilidade e backup.

## 🛠️ Tecnologias Utilizadas

* **Linguagem**: Python 3.13 (compatível com 3.8+).
* **Framework Web**: Flask.
* **Banco de Dados**: SQLite3.
* **Frontend**: HTML5 e CSS3 com design responsivo e modo escuro.

## 🔧 Como Executar o Projeto

1. **Instale as dependências**:
   ```bash
   pip install flask
Prepare o Banco de Dados:
Certifique-se de que o arquivo biblioteca_comunitaria.db está na raiz ou execute o script de atualização:

Bash

python atualizar_banco.py
Inicie o Servidor:

Bash

python app.py
Acesse no Navegador:
Abra no seu endereço IPV4 privado

🔐 Credenciais de Acesso (Padrão)
Usuário: admin

Senha: biblioteca2026

📁 Estrutura do Projeto
app.py: Servidor principal e rotas Flask.

templates/: Arquivos HTML do sistema.

biblioteca_comunitaria.db: Arquivo do banco de dados SQLite.

atualizar_banco.py: Script de manutenção e criação de tabelas.

Desenvolvido por Matheus - Estudante de ADS na Anhanguera.