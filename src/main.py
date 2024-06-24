# from chroma_search import pesquisa
from flask import Flask
from views import views
import sqLite


app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
