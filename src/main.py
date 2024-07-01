# COMPONENTES DO GRUPO:
# MARCO AURÉLIO TIAGO FILHO
# JOÃO VICTOR FERREIA ABRÊU
# BERNARDO FERRI SCHIRMER

from flask import Flask
from views import views


app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")


if __name__ == "__main__":
    app.run(debug=True, port=8000)