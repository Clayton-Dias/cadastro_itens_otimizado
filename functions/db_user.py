from flask import g


def get_user(mysql, form):
    # Procurar usuário pelo email e senha

    sql = '''
            SELECT *,
                -- Gera uma versão das datas em pt-BR para salvar no cookie
                DATE_FORMAT(u_data, '%%d/%%m/%%Y às %%H:%%m') AS u_databr,
                DATE_FORMAT(u_nascimento, '%%d/%%m/%%Y') AS u_nascimentobr
            FROM usuario
            WHERE u_email = %s
                AND u_senha = SHA1(%s)
                AND u_status = 'on'
        '''
    cur = mysql.connection.cursor()
    cur.execute(sql, (form['email'], form['senha'],))
    usuario = cur.fetchone()
    cur.close()

    return usuario


def search_user(mysql, form):
    # Verificar o email já está cadstrado
        
        # Verifica se usuário já está cadastrado, pelo e-mail
        sql = "SELECT u_id, u_status FROM usuario WHERE u_email = %s AND u_status != 'del'"
        cur = mysql.connection.cursor()
        cur.execute(sql, (form['email'],))
        rows = cur.fetchall()
        cur.close()

        return rows

def create_user(mysql, form):
    # Salva dados do novo usuário cadastrado no banco de dados

    sql = "INSERT INTO usuario (u_nome, u_nascimento, u_email, u_senha) VALUES (%s, %s, %s, SHA1(%s))"
    cur = mysql.connection.cursor()
    cur.execute(
            sql, (
                    form['nome'],
                    form['nascimento'],
                    form['email'],
                    form['senha'],
                )
            )
    mysql.connection.commit()
    cur.close()

    return True

def search_date_user(mysql, form):
    # Procurar o ID do usuário pelo email e data de nascimento
        
        sql = '''
            SELECT u_id
            FROM usuario
            WHERE u_email = %s
                AND u_nascimento = %s
                AND u_status = 'on'
        '''
        cur = mysql.connection.cursor()
        cur.execute(sql, (form['email'], form['nascimento'],))
        row = cur.fetchone()
        cur.close()
    
        return row


def upadte_password(mysql, novasenha, row):
    # Atualiza a senha do usuário no banco de dados
    
    sql = "UPDATE usuario SET u_senha = SHA1(%s) WHERE u_id = %s"
    cur = mysql.connection.cursor()
    cur.execute(sql, (novasenha, row['u_id'],))
    mysql.connection.commit()
    cur.close()

def delete_user(mysql):
    
    # Apaga completamente o usuario (CUIDADO!)
    # sql = 'DELETE FROM usuario WHERE t_id = %s'
    # Altera o status do usuario para 'del' (Mais seguro)

    sql = "UPDATE usuario SET u_status = 'del' WHERE u_id = %s"
    cur = mysql.connection.cursor()
    cur.execute(sql, (g.usuario['id'],))
    mysql.connection.commit()
    cur.close()