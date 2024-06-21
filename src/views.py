import json

from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from sqLite import register_user, logar, esquece_senha, registra_artigo
import arxiv_seach
views = Blueprint(__name__, "views")


@views.route("/")
def home():
    return render_template("index.html")



@views.route("/forgot_password")
def forgot_password():
    email = request.args.get("email")  # confere se foi recebido um email como parametro
    # se não foi, renderiza a tela pedindo apenas o email
    if email is not None:
        esquece_senha(email)
        return render_template("forgot_password.html", success="false")
    # se foi, renderiza também a mensagem de sucesso, e envia o email para o usuario
    return render_template("forgot_password.html", success="true")


@views.route("/register_user")
def register():
    return render_template("register_user.html", success="true")



@views.route("/menu", methods=["GET", "POST"])
def menu():
    if request.method == "GET":
        arg = request.args
        cpf = arg.get("cpf")
        error = "false"
        if cpf is None:
            # se não tiver o cpf no link, jogar como erro
            error = "true"

    elif request.method == "POST":
        form = request.form
        cpf = form.get('user')
        password = form.get('psswrdHsh')
        print(cpf,password)
        status = logar(cpf, password)
        print(status)
        error = "false"
        if status[0]:
            return render_template("home.html", cpf=cpf, login_error="false")
        return render_template("home.html", cpf=cpf, login_error="true")
    return render_template("home.html", cpf=cpf, login_error=error)

    # botar codigo que confirma se o usuario é valido
    # se usuario não for valido, mandar para a pagina de login de novo



@views.route("/search", methods=["GET"])
def search_articles():
    cpf = ""
    if request.method == "GET":
        arg = request.args
        query = arg.get("search")
        search_total = arg.get("total_search")
        cpf = arg.get("cpf")
        if query is not None and search_total is not None:
            return render_template("search_articles.html", cpf=cpf, query=query, total=search_total)
    return render_template("search_articles.html", cpf=cpf, query="", total=0)


@views.route("/saved", methods=["GET", "POST"])
def saved_articles():
    return render_template("saved_articles.html")

@views.route("/change_password", methods=["GET", "POST"])
def change_password():
    arg = request.args
    cpf = arg.get('cpf')
    return render_template("menu.html", cpf=cpf, login_error="false")


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
    register_user(username, age, cpf, email, cep_string, password)
    return render_template("register_user.html", success="false")
    # return redirect(url_for("views.home"))


@views.route("/json", methods=["GET"])
def get_json():
    args = request.args
    search_query = args.get("search")
    search_size = int(args.get("total"))
    # Realizar a pesquisa e salvar numa lista nova
    artigos = arxiv_seach.search(search_query, search_size, "12345667764")
    lista = list()
    for artigo in artigos:
        json.dumps(lista.append(artigo.dict()))
        registra_artigo(artigo)

    return lista


@views.route("/data")
def get_data():
    data = request.json
    return jsonify(data)


@views.route("/go-to-gome")
def go_to_home():
    return redirect(url_for("views.get_json"))
