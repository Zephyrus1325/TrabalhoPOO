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
