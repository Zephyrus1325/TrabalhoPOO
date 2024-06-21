import sqlite3


def register_user(nome, idade, CPF, email, CEP, senha):
    # Conecta ao banco de dados SQLite (ou cria se ele não existir)
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    # Cria a tabela 'usuarios' se ela não existir
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER NOT NULL,
        CPF TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL,
        CEP TEXT NOT NULL,
        senha TEXT NOT NULL
    )
    ''')

    try:
        # Insere os dados do usuário na tabela 'usuarios'
        cursor.execute('''
        INSERT INTO usuarios (nome, idade, CPF, email, CEP, senha)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (nome, idade, CPF, email, CEP, senha))
        # Confirma a transação
        conn.commit()
        return True, None  # Sucesso, sem erro
    except sqlite3.IntegrityError:
        return False, 1  # Erro: CPF já cadastrado
    except Exception:
        return False, 2  # Outro erro
    finally:
        # Fecha a conexão
        conn.close()


def esquece_senha(email):

    from util import enviar_email
    from util import gerar_senha

    sim, erro_email_existe = email_existe(email)

    if sim:
        # Conecta ao banco de dados
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()

        try:
            # Comando SQL - atualização com condição para CPF e senha
            atualizar_senha = '''
            UPDATE usuarios
            SET senha = ?
            WHERE email = ?
            '''
            nova_senha = gerar_senha()  # Gera uma nova senha
            cursor.execute(atualizar_senha, (nova_senha, email))  # Atualiza a pswd no db
            conn.commit
            enviar_email(email, nova_senha)  # Envia nova senha para o e-mail
            return True, 0  # Operação bem-sucedida
        except Exception:
            return False, 3  # Código de erro para qualquer outro erro
        finally:
            # Fecha a conexão com o banco de dados
            cursor.close()
            conn.close()
    else:
        return erro_email_existe  # Retorna o código de erro - 6


def buscar_email_por_cpf(CPF):
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()

        # Consulta SQL para buscar o e-mail pelo CPF
        consulta = 'SELECT email FROM clientes WHERE cpf = ?'

        # Executar a consulta SQL com o CPF fornecido
        cursor.execute(consulta, (CPF,))

        # Obter o resultado da consulta
        resultado = cursor.fetchone()

        # Fechar o cursor e a conexão com o banco de dados
        cursor.close()
        conn.close()

        # Verificar se o e-mail foi encontrado e retorná-lo
        if resultado:
            return True, str(resultado[0])  # Retorna o e-mail, sem erro
        else:
            return False, None  # não encontrou, retorna falso, sem erro
    except Exception:
        return False, 45  # Retorna o erro


def email_existe(email):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT 1 FROM usuarios WHERE email = ?', (email,))
        result = cursor.fetchone()
        if result:
            return True, None  # E-mail encontrado no banco de dados, sem erro
        else:
            return False, None  # E-mail não encontrado, sem erro
    except Exception:
        return False, 6  # Código de erro
    finally:
        conn.close()  # Fecha a conexão com o banco de dados


def cpf_existe(CPF):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT 1 FROM usuarios WHERE CPF = ?', (CPF,))
        result = cursor.fetchone()
        if result:
            return True, None  # CPF encontrado no banco de dados, sem erro
        else:
            return False, None  # CPF não encontrado, sem erro

    except Exception:
        return False, 69  # Retorna 69 em caso de erro
    finally:
        conn.close()


def logar(CPF, senha):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT 1 FROM usuarios WHERE CPF = ? AND senha = ?', (CPF, senha))
        result = cursor.fetchone()
        if result:
            return True, None
        else:
            return False, None  # senha inválida -- passar o cpf_existe antes
    except Exception:
        return False, 89  # código de erro


def registra_artigo(artigo):
    # Conecta ao banco de dados SQLite (ou cria se ele não existir)
    conn = sqlite3.connect('artigos.db')  # fazer tudo no mesmo arquivo? docs e usuarios?
    cursor = conn.cursor()

    # Cria a tabela 'usuarios' se ela não existir
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS artigos (
        identifier TEXT NOT NULL PRIMARY KEY,
        title TEXT NOT NULL,
        summary  TEXT NOT NULL,
        link TEXT NOT NULL,
        cpf_user TEXT NOT NULL,
        search_query TEXT NOT NULL,
    )
    ''')

    try:
        # Insere os dados do usuário na tabela 'usuarios'
        cursor.execute('''
        INSERT INTO artigos (identifier, title, summary, link, cpf_usar, search_query)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (artigo.identifier, artigo.title, artigo.summary, artigo.link, artigo.cpf_user, artigo.search_query))
        # Confirma a transação
        conn.commit()
        return True, None  # Sucesso, sem erro
    except sqlite3.IntegrityError:
        return False, 32  # Erro: id já cadastrado ou outro erro de integridade
    except Exception:
        return False, 12  # Outro erro
    finally:
        # Fecha a conexão
        conn.close()
