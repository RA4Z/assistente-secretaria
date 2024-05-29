import win32com.client
import os
import requests


class Outlook:
    def __init__(self):
        self.outlook = win32com.client.Dispatch("Outlook.Application")

    def send_email(self, subject, to="", body="", cc="", bcc="", attachments=None, html_body_table=""):
        self.mail = self.outlook.CreateItem(0)  # 0 significa email
        self.mail.Display()  # Abre a janela de composição de e-mail

        signature = self.get_outlook_signature(self.mail)  # Obtém a assinatura do Outlook
        body += "<br>" + html_body_table + "<br>" + signature  # Adiciona a assinatura ao corpo do e-mail

        self.mail.Subject = subject
        self.mail.To = to
        self.mail.CC = cc
        self.mail.BCC = bcc
        self.mail.HTMLBody = body

        if attachments:
            if isinstance(attachments, str):  # Se houver apenas um anexo
                if os.path.exists(attachments.strip()):
                    self.mail.Attachments.Add(attachments.strip())
            elif isinstance(attachments, list):  # Se houver múltiplos anexos
                for attachment in attachments:
                    if os.path.exists(str(attachment).strip()):
                        self.mail.Attachments.Add(str(attachment).strip())

        #mail.Send()
    

    def get_outlook_signature(self, mail):
        # Obtém a assinatura do Outlook
        try:
            signature = mail.HTMLbody
        except AttributeError:
            signature = ""
        return signature

if __name__ == "__main__":
    outlook_sender = Outlook()

    # Exemplo de uso:
    subject = "E-mail Subject"
    to = "robertn@weg.net"
    body = "E-mail Body"
    cc = "robertn@weg.net"
    bcc = "robertn@weg.net"
    attachments = [""]

    outlook_sender.send_email(subject, to, body, cc, bcc, attachments)
