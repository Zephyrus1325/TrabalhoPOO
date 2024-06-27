import chromadb
import arxiv_search as arxiv
import sqLite

#Criar ou adicionar um novo banco de dados
def adicionar_artigo (artigos):
    chclient = chromadb.PersistentClient(path = "database")
    cpf_usuario = artigos[0].cpf_user
    colecao_user = chclient.get_or_create_collection(name= cpf_usuario)

    resumos = list()
    ids = list()
    for artigo in artigos:
        resumos.append(artigo.summary)
        ids.append(artigo.identifier)
    colecao_user.add(
        documents=resumos, #Descricao dos resumos
        ids=ids #ID da colecao
    )


#Pegar o banco de dados e fazer uma pesquisa nele
def pesquisa(keyword, quantidade, cpf_user):

    chclient = chromadb.PersistentClient(path = "database")    # Inicialização
    collection = chclient.get_collection(name= cpf_user) # Coleção para guardar os embeddings
    
    # Input do User
    results = collection.query(
        query_texts=[str(keyword)],  # Prompt de pesquisa
        n_results= int(quantidade),  # Quantos Resultados
    )

    return results['ids'][0] #Retorna os IDs


#Pega a lista de artigos do arxiv e coloca na database do chrmadb
def pesquisar_artigos (keyword, quantidade, cpf_user):

    lista_artigos = arxiv.search(keyword, quantidade, cpf_user)

    adicionar_artigo(lista_artigos)

    for art in lista_artigos:
        sqLite.registra_artigo(art)

    lista_id = pesquisa(keyword, quantidade, cpf_user)

    lista_results = []
    for id in lista_id:
        lista_results.append(sqLite.procura_artigo(id, cpf_user)[0])
    return lista_results


def pesquisar_salvos(keyword, quantidade, cpf):
    ids = pesquisa(keyword, quantidade, cpf)
    ids_out = []
    for id in ids:
        artigo = sqLite.procura_artigo(id, cpf)[0]
        if artigo is not False:
            ids_out.append(artigo)
    return ids_out