import smtplib
import os
import ssl
import smtplib
from email.message import EmailMessage

#Sends a basic contact form
def send_message(s_email, message):
    email_sender = os.environ.get("SERVER_EMAIL")
    email_receiver = os.environ.get("STUYOLY_EMAIL")
    psk = os.environ.get("SERVER_EMAIL_PSK")

    #Prepare email
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = "Contact Form Submission"
    em.set_content("From: " + s_email + "\n" + message)

    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ctx) as smtp:
        smtp.login(email_sender, psk)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

    return "SUCCESS"






