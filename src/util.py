# COMPONENTES DO GRUPO:
# MARCO AURÉLIO TIAGO FILHO
# JOÃO VICTOR FERREIA ABRÊU
# BERNARDO FERRI SCHIRMER

import secrets
import smtplib
import sqLite
from email.mime.text import MIMEText # pra codificar as mensagen

def gerar_senha():
    nova_senha = secrets.token_urlsafe(5)
    return nova_senha


def enviar_email(email_usuario, nova_senha):
    username = sqLite.buscar_nome(email_usuario)
    sender = "geraldosena371@gmail.com"
    body = f"Olá {username}!, sua nova senha é: {nova_senha}"
    subject = "Nova senha"
    password = "srrzlnneqxucivkb"  # Senha do remetente

    # Criação da mensagem MIME
    msg = MIMEText(body)
    msg['Subject'] = subject   # Assunto do email
    msg['From'] = sender       # Remetente
    msg['To'] = email_usuario  # Destinatário

    try:
        # Conexão com o servidor SMTP do Gmail usando SSL na porta 465
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            # Login no servidor SMTP
            smtp_server.login(sender, password)
            # Envio do email
            smtp_server.sendmail(sender, email_usuario, msg.as_string())
        return True, 44
    except smtplib.SMTPException:
        return False, 97    # erro na smtplib
    except Exception:
        return False, 99    # outro erro