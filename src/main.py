from flask import Flask
from views import views
import sqLite

from artigo import Artigo
import chroma_search as chr


app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")


if __name__ == "__main__":
    # app.run(debug=True, port=8000)
    print(chr.pesquisar_artigos("", 3, "456554656"))