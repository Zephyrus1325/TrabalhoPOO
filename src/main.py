# from chroma_search import pesquisa
from flask import Flask
from views import views
import sqLite
import arxiv_seach

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")


if __name__ == "__main__":
    arxiv_seach.search("test")
    app.run(debug=True, port=8000)

    # user_input = input("Digite uma palavra para a Busca: ")
    # quantia = int(input("Digite quantas buscas a serem feitas: "))

    # resultado = pesquisa(user_input, quantia)

    # print(resultado)
