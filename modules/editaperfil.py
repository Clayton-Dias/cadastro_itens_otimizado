from flask import g, redirect, render_template, request, url_for

from functions.db_user import edit_profile, edit_profile_password, get_all_date_user


def mod_edita_perfil(mysql):
    # Se o usuário não está logado redireciona para a página de login
    if g.usuario == '':
        return redirect(url_for('login'))

    if request.method == 'POST':

        form = dict(request.form)

        # print('\n\n\n FORM:', form, '\n\n\n')

        edit_profile(mysql, form)

        # Se pediu para trocar a senha
        edit_profile_password(mysql,form)

        return redirect(url_for('logout'))

    # Recebe dados do usuário   
    row = get_all_date_user(mysql)

    # print('\n\n\n USER:', row, '\n\n\n')

    pagina = {
        'titulo': 'CRUDTrecos - Erro 404',
        'usuario': g.usuario,
        'form': row
    }
    return render_template('editaperfil.html', **pagina)