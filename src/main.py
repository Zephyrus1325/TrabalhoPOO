from flask import Flask
from views import views
import sqLite

from artigo import Artigo
import chroma_search as chr


app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")


if __name__ == "__main__":
    # app.run(debug=True, port=8000)

    #EXEMPLO DE TESTE PARA O CHROMADB PARA CHECAR SE RETORNA OS IDS NA ORDEM 02 - 01
    artigo1 = Artigo(ident= "01", title="Coding in Java", resume="Learn the basics of Java", link="https.Java.com", cpf_user="3456543", search_query="Java")
    chr.adicionar_artigo(artigo1)

    artigo1 = Artigo(ident= "02", title="Coding in Python", resume="Learn the basics of Python", link="https.python.com", cpf_user="3456543", search_query="Python")

    chr.adicionar_artigo(artigo1)
    chr.pesquisa("Python", "2", "3456543")