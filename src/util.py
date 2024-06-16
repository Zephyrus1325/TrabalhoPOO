def gerar_senha():
    import secrets
    nova_senha = secrets.token_urlsafe(8)
    return nova_senha



def enviar_email(email_usuario, nova_senha):
    import smtplib
    from email.mime.text import MIMEText  #pra codificar as mensagen 
    sender = "geraldosena371@gmail.com"
    body = f"Sua nova senha: {nova_senha}"
    subject = "Nova senha"
    password = "srrzlnneqxucivkb"  # Senha do remetente

    # Criação da mensagem MIME
    msg = MIMEText(body)
    msg['Subject'] = subject  # Assunto do email
    msg['From'] = sender  # Remetente
    msg['To'] = email_usuario  # Destinatário

    try:
        # Conexão com o servidor SMTP do Gmail usando SSL na porta 465
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            # Login no servidor SMTP
            smtp_server.login(sender, password)
            # Envio do email
            smtp_server.sendmail(sender, email_usuario, msg.as_string())
        return True, 44
    except smtplib.SMTPException as e:
        return False, 97 #erro na smtplib
    except Exception as e:
        return False, 99 #outro erro

