from flask import Flask, render_template, request, redirect, url_for, flash, session
from modulos.instrumentos import pegar_todos_instrumentos, criar_conexao # Importe suas funções
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import sqlite3

app = Flask(__name__)
app = Flask(__name__)
app.secret_key = "chave_secreta_para_projeto_extensao" # Necessário para o flash funcionar
USUARIOS = {"admin": "biblioteca2026"}

@app.route('/')
def index():
    if not session.get('logado'):
        return redirect(url_for('login'))
    
    termo = request.args.get('busca', '').strip()
    conn = criar_conexao()
    cursor = conn.cursor()

    # Selecionamos as colunas NOMINALMENTE para garantir a ordem
    colunas = "id, tipo, marca, aluno_responsavel, contato_aluno, data_emprestimo, cidade, bairro, rua, numero_casa"
    
    if termo:
        sql = f"SELECT {colunas} FROM instrumentos WHERE tipo LIKE ? OR marca LIKE ? OR aluno_responsavel LIKE ?"
        filtro = f'%{termo}%'
        cursor.execute(sql, (filtro, filtro, filtro))
    else:
        cursor.execute(f"SELECT {colunas} FROM instrumentos")

    instrumentos = cursor.fetchall()
    conn.close()
    return render_template('index.html', instrumentos=instrumentos)


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if not session.get('logado'): return redirect(url_for('login'))
    if request.method == 'POST':
        # 1. Captura os dados do formulário
        tipo = request.form['tipo'].strip().title()
        marca = request.form['marca'].strip().title()
        modelo = request.form['modelo'].strip().title()
        numero = request.form['numero'].strip().title()
        origem = request.form['origem'].strip().title()
        aluno = request.form['aluno'].strip().title()
        telefone = request.form.get('telefone')
        cidade = request.form.get('cidade').strip().title()
        bairro = request.form.get('bairro').strip().title()
        rua = request.form.get('rua').strip().title()
        numero_casa = request.form.get('numero_casa')
                
        # 2. Lógica da Data: Se já cadastrar com um aluno, gera a data de hoje
        data_posse = datetime.now().strftime('%d/%m/%Y') if aluno else ""

        conn = criar_conexao()
        cursor = conn.cursor()
        
        # 3. SQL atualizado para incluir a 8ª coluna (data_emprestimo)
        sql = '''INSERT INTO instrumentos
                (tipo, marca, aluno_responsavel, data_emprestimo, contato_aluno, cidade, bairro, rua, numero_casa)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        
        # 4. Executa passando os 12 valores na ordem exata
        cursor.execute(sql, (tipo, marca, aluno, data_posse, telefone, cidade, bairro, rua, numero_casa))
        
        conn.commit()
        conn.close()
        
        flash("✅ Instrumento cadastrado com sucesso!", "success")
        return redirect(url_for('index'))
    
    return render_template('cadastrar.html')


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if not session.get('logado'):
        return redirect(url_for('login'))

    conn = criar_conexao()
    cursor = conn.cursor()

    if request.method == 'POST':
        # 1. Captura os dados do formulário
        tipo = request.form['tipo']
        marca = request.form['marca']
        aluno = request.form['aluno']
        contato = request.form['contato']
        data_emp = request.form['data_emprestimo']
        cidade = request.form['cidade']
        bairro = request.form['bairro']
        rua = request.form['rua']
        numero = request.form['numero_casa']

        # 2. SQL de Update
        sql = '''UPDATE instrumentos SET
                tipo=?, marca=?, aluno_responsavel=?, contato_aluno=?,
                data_emprestimo=?, cidade=?, bairro=?, rua=?, numero_casa=?
                WHERE id=?'''
        
        cursor.execute(sql, (tipo, marca, aluno, contato, data_emp, cidade, bairro, rua, numero, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    # 3. Se for GET, busca os dados para preencher o formulário
    # Usamos a ordem exata para bater com os índices inst[x] do editar.html
    sql_select = '''SELECT id, tipo, marca, modelo, numero, origem,
                        aluno_responsavel, contato_aluno, data_emprestimo,
                        cidade, bairro, rua, numero_casa
                    FROM instrumentos WHERE id = ?'''
    
    cursor.execute(sql_select, (id,))
    instrumento = cursor.fetchone()
    conn.close()

    return render_template('editar.html', inst=instrumento)


@app.route('/remover/<int:id>')
def remover_web(id):
    if not session.get('logado'): return redirect(url_for('login'))
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM instrumentos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash("🗑️ Instrumento removido com sucesso!", "danger")
    return redirect(url_for('index'))


@app.route('/buscar')
def buscar():
    if not session.get('logado'): return redirect(url_for('login'))
    termo = request.args.get('aluno', '').lower()
    conn = criar_conexao()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # Busca tanto no tipo do instrumento quanto no nome do aluno
    cursor.execute("SELECT * FROM instrumentos WHERE LOWER(tipo) LIKE ? OR LOWER(aluno_responsavel) LIKE ?", 
                (f'%{termo}%', f'%{termo}%'))
    resultados = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return render_template('index.html', instrumentos=resultados)


@app.route('/cautela/<int:id>')
def cautela(id):
    if not session.get('logado'):
        return redirect(url_for('login'))

    conn = criar_conexao()
    cursor = conn.cursor()
    # Buscamos a ordem exata das 13 colunas para bater com o HTML
    cursor.execute('''SELECT id, tipo, marca, modelo, numero, origem,
                            aluno_responsavel, contato_aluno, data_emprestimo,
                            cidade, bairro, rua, numero_casa
                    FROM instrumentos WHERE id = ?''', (id,))
    
    instrumento = cursor.fetchone()
    conn.close()

    if instrumento:
        from datetime import datetime
        data_hoje = datetime.now().strftime('%d/%m/%Y')
        return render_template('cautela.html', inst=instrumento, data_hoje=data_hoje)
    
    return "Instrumento não encontrado", 404


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        if usuario in USUARIOS and USUARIOS[usuario] == senha:
            session['logado'] = True
            return redirect(url_for('index'))
        flash("Usuário ou senha inválidos!", "danger")
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("Sessão encerrada com sucesso.", "info")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)