class Artigo:
    identifier = ""
    title = ""
    resume = ""
    link = ""
    cpf_user = ""
    search_query = ""

    def __init__(self, ident, title, resume, link, cpf_user, search_query):
        self.identifier = ident
        self.title = title
        self.resume = resume
        self.link = link
        self.cpf_user = cpf_user
        self.search_query = search_query

    def print(self):
        print(self.identifier, self.title, self.resume, self.link)

    def dict(self):
        return {"id": self.identifier, "title": self.title, "summary": self.resume, "link": self.link}