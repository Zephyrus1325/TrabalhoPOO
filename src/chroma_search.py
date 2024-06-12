import chromadb



def pesquisa(keyword, quantidade):

    chclient = chromadb.Client()    # Inicialização
    collection = chclient.get_or_create_collection(name="my_collection") # Coleção para guardar os embeddings

    # Mapear IDs para Docs
    database = {
        "Laser Cut": ({"Nome": "Artigo sobre corte a laser"}, {"Conteudo": "Corte a laser e uma tecnica para producao de artigos e coisas assim, seria interessante aprender a mexer com isso direito e coisa e tal"}),
        "Assembly": "This is a document about assembly",
        "Python": "This is a document about python",
        "Java": "This is a document about java"
    }

    # Atualizar a coleção com os documentos da database
    collection.upsert(
        documents=list(database.values()), # Lista de Todos os conteudos
        ids=list(database.keys()) # Lista de IDs
    )

    # Input do User
    results = collection.query(
        query_texts=[str(keyword)],  # Prompt de pesquisa
        n_results=quantidade,        # Quantos Resultados
    )

    results.pop('metadatas')    # Remover os conteudos
    results.pop('embeddings')   # que não retornam
    results.pop('uris')         # valores (None)
    results.pop('data')         #

    # Criar lista de dicionarios
    lista_final = []
    
    for i in range(len(results['ids'][0])):
        dicionario = {}
        for chave, lista in results.items():
            dicionario[chave] = lista[0][i]
        lista_final.append(dicionario)
    
    return lista_final

