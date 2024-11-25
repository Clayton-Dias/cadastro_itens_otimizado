from flask import g, make_response, redirect, url_for

from functions.db_treco import delete_treco_by_user
from functions.db_user import delete_user


def mod_apaga_usuario(mysql):

    # Apaga um usuário do sistema
    # Também apaga todos os seus "trecos"

    # Se o usuário não está logado redireciona para a página de login
    if g.usuario == '':
        return redirect(url_for('login'))

    # Configura o status do usuário para 'del' no banco de dados
    delete_user(mysql)

    # Configura o status dos itens do usuário para 'del' no banco de dados
    delete_treco_by_user(mysql)

    # Página de destino de logout
    resposta = make_response(redirect(url_for('login')))

    # apaga o cookie do usuário
    resposta.set_cookie(
        key='usuario',  # Nome do cookie
        value='',  # Apara o valor do cookie
        max_age=0  # A validade do cookie é ZERO
    )

    # Redireciona para login
    return resposta