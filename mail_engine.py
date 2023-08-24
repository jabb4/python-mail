import smtplib
from email import message
import gnupg


def encrypt_message(msg):
    gpg = gnupg.GPG()

    ### points to recivers public key ###
    with open("reciverPublicKey", "r") as rPubKey:
        r_public_key = rPubKey.read()

    r_public_key = gpg.import_keys(r_public_key)

    if r_public_key.count == 0:
        return 0
    else:
        key_fingerprint = r_public_key.fingerprints[0]

    return str(gpg.encrypt(msg, key_fingerprint, always_trust=True))


def send_mail(mail_reciver, mail_subject, mail_message):
    ### What smtp server your mail is using ###
    ### Outlook has smtp.office365.com ###
    smtp_server = "smtp.office365.com"

    ### What port your smtp server uses ###
    ### Outlook has 587 ###
    smtp_port = 587

    ### What mail you are sending from (login credentials) ###
    mail_sender = "mail@outlook.com"

    ### What password that mail has (login credentials) ###
    mail_sender_password = "password"

    mail = message.Message()
    mail.add_header("from", mail_sender)
    mail.add_header("to", mail_reciver)
    mail.add_header("subject", mail_subject)
    mail.set_payload(mail_message)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(mail_sender, mail_sender_password)
        server.sendmail(mail_sender, mail_reciver, mail.as_string())

        return "Success: Message was sent!"
    except:
        return "ERROR: Message wasn't able to be sent!"