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
    if not session.get('logado'): return redirect(url_for('login'))
    conn = criar_conexao()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM instrumentos")
    instrumentos = cursor.fetchall()
    conn.close()
    return render_template('index.html', instrumentos=instrumentos)


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if not session.get('logado'): return redirect(url_for('login'))
    if request.method == 'POST':
        # 1. Captura os dados do formulário
        tipo = request.form['tipo']
        marca = request.form['marca']
        modelo = request.form['modelo']
        numero = request.form['numero']
        origem = request.form['origem']
        aluno = request.form['aluno']
        contato = request.form['contato']
        
        # 2. Lógica da Data: Se já cadastrar com um aluno, gera a data de hoje
        data_posse = datetime.now().strftime('%d/%m/%Y') if aluno else ""

        conn = criar_conexao()
        cursor = conn.cursor()
        
        # 3. SQL atualizado para incluir a 8ª coluna (data_emprestimo)
        sql = '''INSERT INTO instrumentos
                (tipo, marca, modelo, numero, origem, aluno_responsavel, contato_aluno, data_emprestimo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
        
        # 4. Executa passando os 8 valores
        cursor.execute(sql, (tipo, marca, modelo, numero, origem, aluno, contato, data_posse))
        
        conn.commit()
        conn.close()
        
        flash("✅ Instrumento cadastrado com sucesso!", "success")
        return redirect(url_for('index'))
    
    return render_template('cadastrar.html')


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if not session.get('logado'): return redirect(url_for('login'))
    conn = criar_conexao()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if request.method == 'POST':
        # 1. CAPTURE O ALUNO PRIMEIRO (Isso resolve o UnboundLocalError)
        aluno = request.form.get('aluno', '')
        data_manual = request.form['data_emprestimo']

        if data_manual:
            data_posse = data_manual
        elif aluno:
            data_posse = datetime.now().strftime('%d/%m/%Y')
        else:
            data_posse = ""
        
        # 2. SÓ AGORA CRIE A DATA baseada no aluno
        data_posse = datetime.now().strftime('%d/%m/%Y') if aluno else ""
        
        
        # 3. CAPTURE O RESTANTE
        tipo = request.form['tipo']
        marca = request.form['marca']
        modelo = request.form['modelo']
        numero = request.form['numero']
        origem = request.form['origem']
        contato = request.form['contato']

        # 4. ATUALIZE O SQL (Certifique-se de que o número de '?' bate com as variáveis)
        sql = """UPDATE instrumentos SET
                tipo=?, marca=?, modelo=?, numero=?, origem=?,
                aluno_responsavel=?, contato_aluno=?, data_emprestimo=?
                WHERE id=?"""
        
        cursor.execute(sql, (tipo, marca, modelo, numero, origem, aluno, contato, data_posse, id))
        conn.commit()
        conn.close()
        flash("📝 Alterações e data salvas!", "success")
        return redirect(url_for('index'))
    
    # Se for GET, busca os dados para o formulário
    cursor.execute("SELECT * FROM instrumentos WHERE id = ?", (id,))
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
def gerar_cautela(id):
    if not session.get('logado'): return redirect(url_for('login'))
    conn = criar_conexao()
    conn.row_factory = sqlite3.Row
    inst = conn.cursor().execute("SELECT * FROM instrumentos WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template('cautela.html', inst=inst, data_hoje=datetime.now().strftime('%d/%m/%Y'))


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