from flask import g, redirect, render_template, request, url_for
from functions.db_user import search_date_user, upadte_password
from functions.geral import gerar_senha

def nova_senha(mysql):

    novasenha = ''
    erro = False

    # Se o usuário está logado, redireciona para a página de perfil
    if g.usuario != '':
        return redirect(url_for('perfil'))

    # Se o formulário foi enviado
    if request.method == 'POST':

        # Obtém dados preenchidos
        form = dict(request.form)

        # Teste de mesa
        # print('\n\n\n FORM:', form, '\n\n\n')

        # Pesquisa pelo email e nascimento informados, no banco de dados
        row = search_date_user(mysql, form)

        # Teste de mesa
        # print('\n\n\n DB:', row, '\n\n\n')

        # Se o usuário não existe
        if row == None:
            # Exibe mensagem no frontend
            erro = True
        else:
            # Gera uma nova senha
            novasenha = gerar_senha()

            # Salva a nova senha no banco de dados
            upadte_password(mysql, novasenha, row)

    # Dados, variáveis e valores a serem passados para o template HTML
    pagina = {
        'titulo': 'CRUDTrecos - Nova Senha',
        'erro': erro,
        'novasenha': novasenha,
    }

    return render_template('novasenha.html', **pagina)