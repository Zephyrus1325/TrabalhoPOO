import arxiv
from artigo import Artigo

def search(query):
    # Construct the default API client.
    client = arxiv.Client()

    # Search for the 10 most recent articles matching the keyword "quantum."
    search = arxiv.Search(
        query="quantum",
        max_results=10,
        sort_by=arxiv.SortCriterion.Relevance
    )

    results = client.results(search)

    list_out = list()
    # `results` is a generator; you can iterate over its elements one by one...
    for r in client.results(search):
        artigo = Artigo(r.entry_id, r.title, r.summary, r.pdf_url, "0", query)
        list_out.append(artigo)
