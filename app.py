from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import os
from functools import wraps
from dotenv import load_dotenv

load_dotenv()  # lê o aquivo .env e carrega tudo como variavel de ambiente

app = Flask(__name__)
# chave secreta para sessões (cookies) do Flask
app.secret_key = os.environ.get("SECRET_KEY", "troque-esta-chave-depois")

# ---- CONFIGURAÇÃO DO BANCO ----
# Lê das variáveis de ambiente se existirem
# Se não existirem, usa os valores padrão (usado no seu PC, local).
DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "database": os.environ.get("DB_NAME", "mural_quadra"),
    "port": int(os.environ.get("DB_PORT", 3306)),
    "charset": "utf8mb4",  # para corrigir os emojis e SE DEUS quiser acentos também!
    "ssl_disabled": os.environ.get("DB_SSL_DISABLED", "False").lower() == "true"
}

# senha do administrador para deletar postS e etc...
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Função que protege rotas (só deixa passar quem escrever as palavrinhas magicas)


def login_necessario(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logado'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# --- ROTA: PÁGINA PRINCIPAL (o mural) ---
@app.route('/')
def index():
    conn = get_connection()
    # dictionary=True -> retorna cada linha como dict
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts ORDER BY criado_em DESC")
    posts = cursor.fetchall()
    cursor.close()
    conn.close()

    # Monta uma lista só com as datas que têm evento marcado, no formato
    # "AA/MM/DD" (que o JavaScript do calendário saiba ler kkkk).
    # Cada data vem junto com o título do aviso, pra mostrar ao passar o mouse.
    datas_ocupadas = [
        {"data": post["data_evento"].isoformat(), "titulo": post["titulo"]}
        for post in posts
        if post["data_evento"]
    ]

    return render_template('index.html', posts=posts, datas_ocupadas=datas_ocupadas, admin_logado=session.get('admin_logado', False))

# ROTA DE LOGIN DO ADMIN


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        senha = request.form['senha']
        if senha == ADMIN_PASSWORD:
            session['admin_logado'] = True
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Senha incorreta. Tente novamente.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

# ROTA DE LOGOUT DO ADMIN


@app.route('/logout')
def logout():
    session.pop('admin_logado', None)
    flash('Logout realizado com sucesso.', 'success')
    return redirect(url_for('index'))

# -- ROTA: CRIAR NOVO AVISO/EVENTO --


@app.route('/novo', methods=['GET', 'POST'])
@login_necessario
def novo_post():
    if request.method == 'POST':
        titulo = request.form['titulo']
        conteudo = request.form['conteudo']
        data_evento = request.form.get('data_evento') or None

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO posts (titulo, conteudo, data_evento) VALUES (%s, %s, %s)",
            (titulo, conteudo, data_evento)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))

    # Se for GET, só mostra o formulário vazio
    return render_template('novo_post.html')


# - ROTA: APAGAR UM AVISO -
@app.route('/deletar/<int:post_id>')
@login_necessario
def deletar_post(post_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id = %s", (post_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':

    # No seu PC roda na porta 5000. No Render, ele informa a porta certa através da variável de ambiente PORT.

    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
