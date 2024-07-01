# COMPONENTES DO GRUPO:
# MARCO AURÉLIO TIAGO FILHO
# JOÃO VICTOR FERREIA ABRÊU
# BERNARDO FERRI SCHIRMER

import arxiv
from artigo import Artigo


# Pesquisa os artigos pelo arxiv, e retorna uma lista com os artigos de resultado
def search(query, total_results, user_cpf):
    # Construct the default API client.
    client = arxiv.Client()

    # Faz a pesquisa de acordo com o query e retorna os resultados de acordo com a relevancia
    search = arxiv.Search(
        query=query,
        max_results=total_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    results = client.results(search)

    # Gerar lista de resultados
    list_out = list()
    for r in client.results(search):
        artigo = Artigo(r.entry_id.replace("http://arxiv.org/abs/", ""), r.title, r.summary, r.pdf_url, user_cpf, query)
        list_out.append(artigo)
    return list_out