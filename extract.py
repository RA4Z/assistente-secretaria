from docx import Document

class Dados():
    def extrair_procedimento(self, filename:str):
        try:
            doc = Document(filename)
            texto = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        except:
            texto = ''
            pass

        return texto
    
