import google.generativeai as genai
from data import historico
from datetime import date
from functions import ultimo_dia_util
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
      Quando aparecer escrito o texto "ANO_ATUAL", substitua por {date.today().year}, quando aparecer escrito o texto "MES_ATUAL", substitua por {date.today().month:02}, quando aparecer escrito o texto "SEMANA_ATUAL", substitua por {date.today().isocalendar().week}, quando aparecer escrito o texto "ULTIMO_DIA_UTIL", substitua por {ultimo_dia_util(date.today())}, quando aparecer escrito o texto "DIA_ATUAL", substitua por {date.today().day:02}
      Quando aparecer escrito o texto "SEM_PASSADO", substitua por {str(int(date.today().strftime('%m'))-1).zfill(2)};
      Formate as datas de 'LastUpdate' dos indicadores em formato de 'dd/mm/yyyy', mantendo a data que se encontra na base de dados.
      Separe o passo a passo para atualizar o indicador em vários tópicos, não fazendo uso de subtópicos, deve estar escrito <topico> na frente de cada tópico;
      Crie um resumo sobre o indicador correspondente ao comando, também informando a última data de atualização do mesmo e se ele está com o status Pendente ou Realizado, além disso mostre o caminho do documento word com o respectivo procedimento;
      SOMENTE USE os dados do documento word com o procedimento do indicador {message} para entregar o resultado.

      Quando aparecer 'Encaminhar EMAIL (', então colocar no mesmo tópico todo o texto até aparecer o ), semelhante ao ultimo tópico de exemplo

      CASO O INDICADOR {message} NÃO EXISTA, ENTÃO NO RESUMO DIGA QUE O INDICADOR NÃO FOI ENCONTRADO E ENTREGUE UM TÓPICO ESCRITO "Error 404";
      Siga o modelo abaixo para o output CASO O INDICADOR EXISTA:
      
       <topico> Abra o arquivo localizado na pasta Q:/GROUPS/...
       <topico> Abra o SAP
       <topico> Acesse a transação ...
       <topico> Insira a variante ...
       <topico> Executar a transação
       <topico> Copiar materiais e inserir no arquivo ...
       <topico> Encaminhar EMAIL(Tópico opcional) ( | Title: ... | Body: ... | To (Campo opcional):... | Copy (Campo opcional):... | CCo (Campo opcional): ... | Attachments (Campo opcional): ... |)

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
  topicos, resumo = ia.send_message('Kanban Diário')
  
  for topico in topicos:
    print(topico)

  print(resumo)
