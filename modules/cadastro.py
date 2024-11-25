from flask import g, redirect, render_template, request, url_for

from functions.db_user import create_user, search_user


def mod_cadastro(mysql):
    jatem = ''
    success = False

    # Se o usuário está logado redireciona para a página de perfil
    if g.usuario != '':
        return redirect(url_for('perfil'))

    if request.method == 'POST':

        form = dict(request.form)

        # Verifica se usuário já está cadastrado, pelo e-mail
        rows = search_user(mysql, form)

        # print('\n\n\n LEN:', len(rows), '\n\n\n')

        if len(rows) > 0:
            # Se já está cadastrado
            if rows[0]['u_status'] == 'off':
                jatem = 'Este e-mail já está cadastrado para um usuário inativo. Entre em contato para saber mais.'
            else:
                jatem = 'Este e-mail já está cadastrado. Tente fazer login ou solicitar uma nova senha.'
        else:
            # Se não está cadastrado, inclui os dados do form no banco de dados
            success = create_user(mysql, form)

    # Dados, variáveis e valores a serem passados para o template HTML
    pagina = {
        'titulo': 'CRUDTrecos - Cadastre-se',
        'jatem': jatem,
        'success': success,
    }

    return render_template('cadastro.html', **pagina)