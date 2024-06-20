from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from util import enviar_email, gerar_senha
from sqLite import register_user
views = Blueprint(__name__, "views")


@views.route("/")
def home():
    return render_template("index.html")



@views.route("/forgot_password")
def forgot_password():
    email = request.args.get("email")  # confere se foi recebido um email como parametro
    # se não foi, renderiza a tela pedindo apenas o email
    if email is not None:
        return render_template("forgot_password.html", success="false")
    # se foi, renderiza também a mensagem de sucesso, e envia o email para o usuario

    # todo remover isso aqui antes de dar deploy
    # enviar_email(email, gerar_senha())
    return render_template("forgot_password.html", success="true")


@views.route("/register_user")
def register():
    return render_template("register_user.html", success="true")



@views.route("/menu", methods=["GET", "POST"])
def menu():
    form = request.form
    cpf = form.get('user')
    password = form.get('psswrdHsh')

    arg = request.args

    if arg.get('cpf') is not None:
        cpf = arg.get('cpf')

    # botar codigo que confirma se o usuario é valido
    # se usuario não for valido, mandar para a pagina de login de novo
    return render_template("home.html", cpf=cpf, login_error="false")


@views.route("/search", methods=["GET", "POST"])
def search_articles():
    form = request.form
    arg = request.args
    return render_template("search_articles.html")


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


@views.route("/json")
def get_json():
    return jsonify({"name": "Tim", "Coolness": 10})


@views.route("/data")
def get_data():
    data = request.json
    return jsonify(data)


@views.route("/go-to-gome")
def go_to_home():
    return redirect(url_for("views.get_json"))
