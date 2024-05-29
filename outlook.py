import win32com.client
import os

class Outlook:
    def __init__(self):
        self.outlook = win32com.client.Dispatch("Outlook.Application")

    def send_email(self, subject, to="", body="", cc="", bcc="", attachments=None, html_body_table=""):
        mail = self.outlook.CreateItem(0)  # 0 significa email
        mail.Display()  # Abre a janela de composição de e-mail

        signature = self.get_outlook_signature(mail)  # Obtém a assinatura do Outlook
        body += "<br>" + html_body_table + "<br>" + signature  # Adiciona a assinatura ao corpo do e-mail

        mail.Subject = subject
        mail.To = to
        mail.CC = cc
        mail.BCC = bcc
        mail.HTMLBody = body

        if attachments:
            if isinstance(attachments, str):  # Se houver apenas um anexo
                if os.path.exists(attachments.strip()):
                    mail.Attachments.Add(attachments.strip())
            elif isinstance(attachments, list):  # Se houver múltiplos anexos
                for attachment in attachments:
                    if os.path.exists(str(attachment).strip()):
                        mail.Attachments.Add(str(attachment).strip())

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
    attachments = ["Q:/GROUPS/BR_SC_JGS_WM_LOGISTICA/PCP/Central/00-Planilha_Padrão/v1.6_Default.xlsm", "Q:/GROUPS/BR_SC_JGS_WM_LOGISTICA/PCP/Central/00-Planilha_Padrão/v1.Funcionalidades.pptx"]

    outlook_sender.send_email(subject, to, body, cc, bcc, attachments)
