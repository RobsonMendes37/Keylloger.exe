import threading
import smtplib
import email.message
import os


# Função para enviar o email em segundo plano
def enviar_email_assincrono(arquivo_anexo):
    t = threading.Thread(target=enviar_email, args=(arquivo_anexo,))
    t.start()

# Função para enviar o email
def enviar_email(arquivo_anexo):  
    corpo_email = """
    
    """

    msg = email.message.EmailMessage()
    msg['Subject'] = "Relatorio De Atividade"
    msg['From'] = 'expotecredes@gmail.com'
    msg['To'] = 'expotecredes@gmail.com'
    password = 'hdibsdjjrxzezmes' 
    msg.add_header('Content-Type', 'text/html')
    msg.set_content(corpo_email)

    # Anexando o arquivo ZIP
    with open(arquivo_anexo, 'rb') as arquivo:
        conteudo_arquivo = arquivo.read()
        nome_arquivo = arquivo_anexo  # Nome que o arquivo terá no e-mail

        # Adicionando o arquivo como anexo
        msg.add_attachment(conteudo_arquivo, maintype='application', subtype='zip', filename=nome_arquivo)

    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        # Login Credentials for sending the mail
        s.login(msg['From'], password)
        s.send_message(msg)
        print('Email enviado com sucesso!')
        os.remove(arquivo_anexo)  # Remover o arquivo ZIP somente após o envio bem-sucedido
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")
    finally:
        s.quit() 



