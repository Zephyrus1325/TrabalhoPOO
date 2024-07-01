# COMPONENTES DO GRUPO:
# MARCO AURÉLIO TIAGO FILHO
# JOÃO VICTOR FERREIA ABRÊU
# BERNARDO FERRI SCHIRMER

# Classe artigo:
# Classe usada majoritariamente para as transações de informações de artigos entre os vários codigos
class Artigo:
    # Definir atributos da classe
    identifier = ""
    title = ""
    summary = ""
    link = ""
    cpf_user = ""
    search_query = ""


    # Construtor da classe Artigo
    def __init__(self, ident, title, resume, link, cpf_user, search_query):
        self.identifier = ident
        self.title = title
        self.summary = resume.replace("\n", " ")
        self.link = link
        self.cpf_user = cpf_user
        self.search_query = search_query


    # Retorna um dicionário com apenas os atributos relevantes do Artigo
    # (vindo do chromadb)
    def dict(self):
        return {"id": self.identifier, "title": self.title, "summary": self.summary, "link": self.link}


    # Retorna um dicionario com todos os atributos do Artigo
    # (inclui CPF do "dono" do artigo e palavra usada para achar ele)
    def dict_full(self):
        return {"id": self.identifier, "title": self.title, "summary": self.summary, "link": self.link, "cpf_user": self.cpf_user, "query": self.search_query}