class Artigo:
    identifier = ""
    title = ""
    summary = ""
    link = ""
    cpf_user = ""
    search_query = ""

    def __init__(self, ident, title, resume, link, cpf_user, search_query):
        self.identifier = ident
        self.title = title
        self.summary = resume.replace("\n", " ")
        self.link = link
        self.cpf_user = cpf_user
        self.search_query = search_query

    def print(self):
        print(self.identifier, self.title, self.summary, self.link)

    def dict(self):
        return {"id": self.identifier, "title": self.title, "summary": self.summary, "link": self.link}

    def dict_full(self):
        return {"id": self.identifier, "title": self.title, "summary": self.summary, "link": self.link, "cpf_user": self.cpf_user, "query": self.search_query}