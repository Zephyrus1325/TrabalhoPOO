# COMPONENTES DO GRUPO:
# MARCO AURÉLIO TIAGO FILHO
# JOÃO VICTOR FERREIA ABRÊU
# BERNARDO FERRI SCHIRMER

import csv

from flask import Blueprint, render_template, request, redirect, url_for, send_file
import sqLite
import chroma_search as chromadb
views = Blueprint(__name__, "views")


# Tela Inicial do Sistema
@views.route("/")
def home():
    # Renderiza apenas a tela inicial
    return render_template("index.html")


# Tela de Esqueci Senha
@views.route("/forgot_password")
def forgot_password():
    email = request.args.get("email")  # confere se foi recebido um email como parametro
    # se não foi, renderiza a tela pedindo apenas o email
    if email is not None:
        sqLite.esquece_senha(email) # Envia mensagem de email com a senha nova
        # Renderiza a tela com mensagem de sucesso
        return render_template("forgot_password.html", success="true")
    # Renderiza a tela sem mensagem de sucesso
    return render_template("forgot_password.html", success="false")


# Tela de Registrar Usuário
@views.route("/register_user")
def register():
    return render_template("register_user.html", success="true")


# Menu Principal do sistema
@views.route("/menu", methods=["GET", "POST"])
def menu():
    error = "true"
    cpf = ""
    # Recebe os parametros via GET
    if request.method == "GET":
        arg = request.args
        cpf = arg.get("cpf")
        error = "false"
        # Checa se o usuário existe no sistema
        nome = sqLite.checar_cpf(cpf)[0]
        print(nome)
        if nome is False or None:
            # Jogar um erro caso não haja o CPF
            return redirect(url_for("views.home"))
        # Caso constrario, renderizar a tela normalmente
        return render_template("home.html", cpf=cpf, login_error="false")
    # Recebe Parametros do Formulário
    elif request.method == "POST":
        form = request.form
        cpf = form.get('user')
        password = form.get('psswrdHsh')
        status = sqLite.logar(cpf, password)
        error = "false"
        if status[0]:
            return render_template("home.html", cpf=cpf, login_error="false")
    return render_template("home.html", cpf=cpf, login_error="true")


# Página de Pesquisa
@views.route("/search", methods=["GET"])
def search_articles():
    cpf = ""
    if request.method == "GET":
        arg = request.args
        query = arg.get("search")
        search_total = arg.get("total_search")
        cpf = arg.get("cpf")

        # confere se não há nenhum parametro de pesquisa
        if query is not None and search_total is not None:
            return render_template("search_articles.html", cpf=cpf, query=query, total=search_total)
    return render_template("search_articles.html", cpf=cpf, query="", total=0)


# Página de artigos salvos
@views.route("/saved", methods=["GET", "POST"])
def saved_articles():
    cpf = ""
    if request.method == "GET":
        arg = request.args
        query = arg.get("search")
        search_total = arg.get("total_search")
        cpf = arg.get("cpf")
        return render_template("saved_articles.html", cpf=cpf, query=query, total=search_total)
    return render_template("saved_articles.html", cpf=cpf, query="", total=0)


# Página de alterar Senha
@views.route("/change_password", methods=["GET", "POST"])
def change_password():

    if request.method == "POST":
        form = request.form
        cpf = form.get('cpf')
        senha_antiga = form.get("old_password")
        senha_nova = form.get("new_password")
        codigo = sqLite.trocar_senha(cpf, senha_antiga, senha_nova)
        return render_template("change_password.html", cpf=cpf, code=codigo[1])
    elif request.method == "GET":
        arg = request.args
        cpf = arg.get('cpf')
        return render_template("change_password.html", cpf=cpf, code=0)
    cpf = ""
    return render_template("change_password.html", cpf=cpf, code=30)


# Link de suporte com que adiciona um usuário
@views.route("/add_user", methods=["GET","POST"])
def add_user():
    form = request.form
    username = form.get("username")
    age = form.get("age")
    cpf = form.get("cpf")
    email = form.get("email")
    cep = form.get("cep")
    street = form.get("street")
    city = form.get("city")
    state = form.get("state")
    password = form.get("password")

    cep_string = f"{cep}, {street}, {city}, {state}"
    sqLite.register_user(username, age, cpf, email, cep_string, password)
    return render_template("register_user.html", success="false")
    # return redirect(url_for("views.home"))


# Link de suporte que retorna um Json com os artigos pesquisados
@views.route("/json", methods=["GET"])
def get_json():
    args = request.args
    cpf = args.get("cpf")
    search_query = args.get("search")
    search_size = int(args.get("total"))
    # Realizar a pesquisa e salvar numa lista nova
    artigos = chromadb.pesquisar_artigos(search_query, search_size, cpf)
    lista = list()
    for artigo in artigos:
        lista.append(artigo.dict())
    return lista


# Link de suporte que retorna os Artigos Salvos de um determinado usuário
@views.route("/get_articles", methods=["GET"])
def get_articles():
    args = request.args
    cpf = args.get("cpf")
    if args.get("search") == "None" or args.get("total") == "None":
        artigos = sqLite.procura_artigos(cpf)[0]
    else:
        search_query = args.get("search")
        search_size = int(args.get("total"))
        artigos = chromadb.pesquisar_salvos(search_query, search_size, cpf)
    output = list()
    for artigo in artigos:
        output.append(artigo.dict_full())
    return output


# Link de suporte que baixa a planilha com os artigos do usuário
@views.route("/download", methods=["GET"])
def download():
    path = "Artigos.csv"
    cpf = request.args.get("cpf")
    with open(path, 'w') as file:
        fields = ["id", "title", "summary", "link", "query", "cpf_user"]
        # procura todos os artigos salvos na conta do usuario
        artigos = sqLite.procura_artigos(cpf)[0]
        lista_dicts = list()
        for artigo in artigos:
            lista_dicts.append(artigo.dict_full())
        writer = csv.DictWriter(file, fieldnames=fields, delimiter=";")
        writer.writeheader()
        writer.writerows(lista_dicts)
    return send_file(path, as_attachment=True)