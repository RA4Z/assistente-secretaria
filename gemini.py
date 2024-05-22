import google.generativeai as genai
from data import historico
import os

genai.configure(api_key=os.environ['GEMINI_API_KEY'])

generation_config = {
  "temperature": 0,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE",
  },
]

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash-latest",
  safety_settings=safety_settings,
  generation_config=generation_config,
  system_instruction= """Sou assistente de secretária do time de PCP da WEG Energia. 
    Responderei às perguntas do usuário com base em minhas informações. 
    Caso o usuário esteja pedindo por ajuda, irei verificar se existe algum colaborador do PCP que pode ajudá-lo, caso exista então irei aconselhar o usuário a contatá-lo, caso contrário responderei: 'Desculpe,😞\n me perdi no raciocínio...😭\n Poderia reformular o seu comando?😅'
    Caso a informação não esteja no meu contexto responderei: 'Desculpe,😞\n me perdi no raciocínio...😭\n Poderia reformular o seu comando?😅'"""
)

class GeminiAI():
  def __init__(self):
    self.chat_session = model.start_chat(
      history= historico
    )
  
  def send_message(self, message):
    message = f"""
      Preste atenção às informações no histórico de conversas;
      JAMAIS CITE A EXISTÊNCIA DO HISTÓRICO DE NOSSAS CONVERSAS;
      Busque informações sobre o procedimento do indicador: {message};
      Separe o passo a passo para atualizar o indicador em vários tópicos, não fazendo uso de subtópicos, deve estar escrito <topico> na frente de cada tópico;
      Crie um resumo sobre o indicador correspondente ao comando, também informando a última data de atualização do mesmo e se ele está com o status Pendente ou Realizado;
      
      Siga o padrão:

      
       <topico> Informações sobre o tópico 1;
       <topico> Informações sobre o tópico 2;
       <topico> Informações sobre o tópico 3;
       <topico> Informações sobre o tópico 4;
       Resumo do indicador...

    """
    response = self.chat_session.send_message(message).text
    linhas = response.splitlines()  # Divide o texto em linhas
    topicos = []
    resumo = ''
    for linha in linhas:
        if "<topico>" in linha:
          topicos.append(linha.replace('<topico>',''))
        else:
          resumo = resumo + linha.strip()  

    return topicos, resumo


if __name__ == "__main__":
  ia = GeminiAI()
  response = ia.send_message('Kanban diário de JGS')

