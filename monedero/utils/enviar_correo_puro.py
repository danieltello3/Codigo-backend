from email.mime.text import MIMEText
import smtplib
from email.mime.multipart import MIMEMultipart
from os import environ
from dotenv import load_dotenv

load_dotenv()

# MIME -> Multi-propose Internet Mail Extensions

mensaje = MIMEMultipart()
password = environ.get("EMAIL_PASSWORD")
mensaje['From'] = environ.get("EMAIL")
mensaje['Subject'] = "Solicitud de olvido de password"  # TITULO del correo


def enviarCorreo(destinatario, nombre, link):
    mensaje['To'] = destinatario
    texto = """Hola, {}!
    Has solicitado recuperar tu password, 
    para tal efecto te enviamos el siguiente link al que deberas ingresar para completar el cambio:

    {}

    Si no fuiste tu, ignora este mensaje

    """.format(nombre, link)
    # luego de definir el cuerpo del correo, lo agregamos al mensaje mediante su metodo attach y en formato MIMEtext en el cual recibira el texto y luego el formato a convertir, si queremos enviar un html, entonces debermos de poner 'html', 'plain' si es solo texto.
    mensaje.attach(MIMEText(texto, 'plain'))

    try:
        servidorSMTP = smtplib.SMTP('smtp.gmail.com', 587)
        servidorSMTP.starttls()
        servidorSMTP.login(mensaje['From'], password)
        servidorSMTP.sendmail(
            from_addr=mensaje['From'],
            to_addrs=mensaje['To'],
            msg=mensaje.as_string()
        )
        servidorSMTP.quit()
        return True
    except Exception as e:
        print(e)
        return False
