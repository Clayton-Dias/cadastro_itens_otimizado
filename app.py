# Importa as dependências do aplicativo
from flask import Flask, abort, g, make_response, redirect, render_template, request, url_for
from flask_mysqldb import MySQL
import json
from functions.geral import calcular_idade, datetime_para_string, gerar_senha, remove_prefixo

from modules.apagausuario import mod_apaga_usuario
from modules.novasenha import nova_senha
from modules.apaga import mod_apaga
from modules.cadastro import mod_cadastro
from modules.edita import mod_edita
from modules.index import mod_index
from modules.login import mod_login
from modules.logout import mod_logout
from modules.novo import mod_novo
from modules.perfil import mod_perfil
from modules.start import mod_start


# Cria um aplicativo Flask chamado "app"
app = Flask(__name__)

# Configurações de acesso ao MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crudtrecos'

# Setup da conexão com MySQL
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['MYSQL_USE_UNICODE'] = True
app.config['MYSQL_CHARSET'] = 'utf8mb4'

# Variável de conexão com o MySQL
mysql = MySQL(app)


@app.before_request
def start():
    mod_start(mysql)   


# Rota raiz, equivalente a página inicial do site (index)
@app.route("/")  
def index():  # Função executada ao acessar a rota raiz
    return mod_index(mysql)   


# Rota para a página de cadastro de novo treco
@app.route('/novo', methods=['GET', 'POST'])
def novo():  # Função executada para cadastrar novo treco
    return mod_novo(mysql=mysql)
    

@app.route('/edita/<id>', methods=['GET', 'POST'])
def edita(id):
    return mod_edita(mysql=mysql, id=id)
   

@app.route('/apaga/<id>')
def apaga(id):
    return mod_apaga(mysql, id)    


@app.route('/login', methods=['GET', 'POST'])  # Rota para login de usuário
def login():
    return mod_login(mysql)


@app.route('/logout')
def logout():
    return mod_logout()


@app.route('/cadastro', methods=['GET', 'POST'])  # Cadastro de usuário
def cadastro():
    return mod_cadastro(mysql)
    

@app.route('/novasenha', methods=['GET', 'POST'])  # Pedido de senha de usuário
def novasenha():
    return nova_senha(mysql)
    

@app.route('/perfil')
def perfil():
    return mod_perfil(mysql)


@app.route('/apagausuario')
def apagausuario():
    return mod_apaga_usuario(mysql)


@app.route('/editaperfil', methods=['GET', 'POST'])
def editaperfil():

    # Se o usuário não está logado redireciona para a página de login
    if g.usuario == '':
        return redirect(url_for('login'))

    if request.method == 'POST':

        form = dict(request.form)

        # print('\n\n\n FORM:', form, '\n\n\n')

        sql = '''
            UPDATE usuario
            SET u_nome = %s,
                u_nascimento = %s,
                u_email = %s
            WHERE u_id = %s
                AND u_senha = SHA1(%s)
        '''
        cur = mysql.connection.cursor()
        cur.execute(sql, (
            form['nome'],
            form['nascimento'],
            form['email'],
            g.usuario['id'],
            form['senha1'],
        ))
        mysql.connection.commit()
        cur.close()

        # Se pediu para trocar a senha
        if form['senha2'] != '':

            sql = "UPDATE usuario SET u_senha = SHA1(%s) WHERE u_id = %s AND u_senha = SHA1(%s)"
            cur = mysql.connection.cursor()
            cur.execute(sql, (
                form['senha2'],
                g.usuario['id'],
                form['senha1'],
            ))
            mysql.connection.commit()
            cur.close()

        return redirect(url_for('logout'))

    # Recebe dados do usuário
    sql = '''
        SELECT * FROM usuario
        WHERE u_id = %s
            AND u_status = 'on'    
    '''
    cur = mysql.connection.cursor()
    cur.execute(sql, (g.usuario['id'],))
    row = cur.fetchone()
    cur.close()

    # print('\n\n\n USER:', row, '\n\n\n')

    pagina = {
        'titulo': 'CRUDTrecos - Erro 404',
        'usuario': g.usuario,
        'form': row
    }
    return render_template('editaperfil.html', **pagina)


@app.errorhandler(404)
def page_not_found(e):
    pagina = {
        'titulo': 'CRUDTrecos - Erro 404',
        'usuario': g.usuario,
    }
    return render_template('404.html', **pagina), 404


# Executa o servidor HTTP se estiver no modo de desenvolvimento
# Remova / comente essas linhas no modo de produção
if __name__ == '__main__':
    app.run(debug=True)
