from flask import Blueprint, render_template, request, jsonify, redirect, url_for

views = Blueprint(__name__, "views")


@views.route("/")
def home():
    return render_template("index.html")


@views.route("/profile")
def profile():
    args = request.args
    name = args.get("name")
    if name != None:
        return render_template("index.html", name=name)
    return render_template("home.html")


@views.route("/forgot_password")
def forgot_password():
    email = request.args.get("email")
    # inserir codigo que manda enviar o email
    if email != None:
        return render_template("forgot_password.html", sucess="false")
    return render_template("forgot_password.html", sucess="true")


@views.route("/menu", methods=["GET","POST"])
def menu():
    form = request.form
    cpf = form.get('user')
    password = form.get('psswrdHsh')
    # botar codigo que confirma se o usuario é valido
    # se usuario não for valido, mandar para a pagina de login de novo
    return render_template("home.html", user=cpf)


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
