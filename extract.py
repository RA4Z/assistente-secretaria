import os
from docx import Document

class Dados():
    def __init__(self):
        pass


    def extrair_texto_da_pasta(self, pasta):
        arquivos_texto = []
        for filename in os.listdir(pasta):
            try:
                if filename.endswith(".docx"):
                    caminho_completo = os.path.join(pasta, filename)
                    doc = Document(caminho_completo)
                    texto = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                    arquivos_texto.append(texto)

            except:
                pass

        return arquivos_texto


    def extrair_procedimento(self, filename:str):
        try:
            doc = Document(filename)
            texto = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        except:
            texto = ''
            pass

        return texto
    
