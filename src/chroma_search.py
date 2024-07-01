# COMPONENTES DO GRUPO:
# MARCO AURÉLIO TIAGO FILHO
# JOÃO VICTOR FERREIA ABRÊU
# BERNARDO FERRI SCHIRMER

import chromadb
import arxiv_search as arxiv
import sqLite


# Criar ou Buscar um banco de dados, e alocar os artigos do ChromaDB
def adicionar_artigo (artigos):

    # Conecta-se ao Banco de dados do usuário
    chclient = chromadb.PersistentClient(path = "database")
    cpf_usuario = artigos[0].cpf_user
    colecao_user = chclient.get_or_create_collection(name= cpf_usuario)

    resumos = list()
    ids = list()

    # Adiciona o resumo e o id dos artigos às suas listas respectivas
    for artigo in artigos:
        resumos.append(artigo.summary)
        ids.append(artigo.identifier)
    
    # Adiciona as informações das listas à database do usuário
    colecao_user.add(
        documents=resumos,
        ids=ids
    )


# Pesquisar no banco de dados do usuário e filtrar os artigos salvos
def pesquisa(keyword, quantidade, cpf_user):

    chclient = chromadb.PersistentClient(path = "database") # Inicialização
    collection = chclient.get_collection(name= cpf_user)    # Pegar a database baseado no cpf do usuário
    
    # Input do Usuário
    results = collection.query(
        query_texts=[str(keyword)], # Prompt de Pesquisa
        n_results= int(quantidade), # Quantos Resultados
    )

    return results['ids'][0]    #Retorna uma lista com os IDs


# Pegar a lista de artigos e colocar na database do ChromaDB
def pesquisar_artigos (keyword, quantidade, cpf_user):

    # Busca a lista de artigos do Arxiv e alocar à database do Chroma
    lista_artigos = arxiv.search(keyword, quantidade, cpf_user)
    adicionar_artigo(lista_artigos)

    # Registra os artigos no SQLite
    for art in lista_artigos:
        sqLite.registra_artigo(art)

    # Busca os IDs dos Artigos
    lista_id = pesquisa(keyword, quantidade, cpf_user)

    lista_results = []

    # Aloca os Artigos em uma Lista
    for id in lista_id:
        lista_results.append(sqLite.procura_artigo(id, cpf_user)[0]) #Retorna um único Artigo
    return lista_results


# Procura de Artigos Salvos no Banco de Dados do SQLite
def pesquisar_salvos(keyword, quantidade, cpf):
    ids = pesquisa(keyword, quantidade, cpf)
    ids_out = []
    for id in ids:
        artigo = sqLite.procura_artigo(id, cpf)[0]
        if artigo is not False:
            ids_out.append(artigo)
    return ids_out