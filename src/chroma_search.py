import chromadb
from artigo import Artigo

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
    results.pop('data')         #

    # Criar lista de IDs
    lista_id = []
    
    for id in range(len(results['ids'][0])):
        lista_id.append (results['ids'] [id])
    return lista_id