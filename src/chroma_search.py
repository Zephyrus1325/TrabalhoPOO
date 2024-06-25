import chromadb
from arxiv_search import search
from artigo import Artigo
from sqLite import registra_artigo, procura_artigo

#Criar ou adicionar um novo banco de dados
def adicionar_artigo (artigo):
    chclient = chromadb.PersistentClient(path = "database")
    cpf_usuario = artigo.cpf_user
    colecao_user = chclient.get_or_create_collection(name= cpf_usuario)

    titulo = str(artigo.title)
    resumo = str(artigo.summary)

    colecao_user.add(
        documents=[resumo], #Descricao dos resumos
        metadatas=[{ #Contem o que vai ser mandado para a database
            "title": titulo,
            "resume": resumo,
        }],
        ids=[artigo.identifier] #ID da colecao
    )


#Pegar o banco de dados e fazer uma pesquisa nele
def pesquisa(keyword, quantidade, cpf_user):

    chclient = chromadb.PersistentClient(path = "database")    # Inicialização
    collection = chclient.get_or_create_collection(name= cpf_user) # Coleção para guardar os embeddings
    
    # Input do User
    results = collection.query(
        query_texts=[str(keyword)],  # Prompt de pesquisa
        n_results= int(quantidade),  # Quantos Resultados
    )

    results.pop('documents')    # Remover os conteudos
    results.pop('embeddings')   # que não retornam
    results.pop('uris')         # valores (None)
    results.pop('data')         

    print(results['ids'][0])
    return results['ids'][0] #Retorna os IDs


#Pega a lista de artigos do arxiv e coloca na database do chrmadb
def pesquisar_artigos (keyword, quantidade, cpf_user):

    lista_artigos = search(keyword, quantidade, cpf_user)

    for art in lista_artigos:
        adicionar_artigo(art)
        registra_artigo(art)

    lista_id = pesquisa(keyword, quantidade, cpf_user)

    lista_results = []
    for id in lista_id:
        lista_results.append(procura_artigo(id, cpf_user)[0])

    return lista_results