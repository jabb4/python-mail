import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Mail():
    """
    This class is used to send emails using the SMTP protocol.

    args:
        smtp_address (str): The address of the SMTP server. (e.g. "smtp.office365.com" or "192.168.1.1")
        smtp_port (int): The port of the SMTP server. (e.g. 25)
        sender (str): The email address of the sender. (e.g. "sender@example.com")
        password (str): The password of the sender. (e.g. "password123")

    methods:
        send_mail: This method sends an email to the receiver with the subject and body.
    """

    def __init__(self, smtp_address, smtp_port, sender, password):

        self.smtp_address = smtp_address
        self.smtp_port = smtp_port
        self.sender = sender
        self.password = password

    def send_mail(self, receiver, subject, body, bcc = [], html = False):
        """
        This method sends an email to the receiver with the subject and body.

        args:
            receiver (str): The email address of the receiver. (e.g. "reciver@example.com")
            subject (str): The subject of the email. 
            body (str): The body of the email.
            bcc (list): A list of email addresses to BCC. (e.g. ["1@example.com", "2@example.com"])
            html (bool): Set to True if the body is in HTML format.
        
        returns:
            tuple: A tuple containing the status if the email was sent successfully. The first element is 1 if the email was sent successfully, 0 otherwise. The second element is a message indicating the status of the email.
        """

        message = MIMEMultipart()
        message["From"] = self.sender
        message["To"] = receiver
        message["Subject"] = subject
        if bcc:
            message["Bcc"] = bcc

        ## Attach the body to the email
        message.attach(MIMEText(body, "plain"))
        if html:
            message.attach(MIMEText(body, "html"))

        ## Create a secure connection with the server and send the email
        try:
            with smtplib.SMTP(self.smtp_address, self.smtp_port) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(self.sender, self.password)
                server.sendmail(self.sender, receiver, message.as_string())
            return (1,"Success: Message was sent!")
        except Exception as e:
            return (0, f"ERROR: Message was not able to be sent! {type(e).__name__}: {e}")