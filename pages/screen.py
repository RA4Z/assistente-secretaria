import flet as ft
import json
import sys
import os
from datetime import date
import pyperclip
import re

config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(config_dir)

from gemini import GeminiAI
from rotinas import run_all
from outlook import Outlook
from components.Aba import Aba
from components.Indicador import Indicador
import pythoncom

class Graphic(ft.UserControl):
  def __init__(self):
    self.app_text = json.load(open(f'pages/text.json', 'r', encoding='utf-8'))
    self.ia = GeminiAI()
    self.logotipo = ft.Image(src="images/logo.png")
    self.loading = ft.Image(src="images/loading.gif", width=75, visible=False)
    ft.app(target=self.main)


  def main(self, page: ft.Page):
    self.page = page  # Armazena a referência para a página
    page.title = self.app_text.get('window_title')
    self.indicador_atual = ''
    self.tabs = Aba(page, self.send_command, self.clean_data)
    self.indicador = Indicador(page, self.finish)

    page.add(
      ft.Row(
        controls=[
          self.logotipo,
          ft.Text(self.app_text.get('main_title'), size=24, text_align=ft.TextAlign.CENTER, weight='bold', expand=True),
        ],
      ),

      ft.Container(
        height=15
      ),
      ft.Row(
        controls=[
          self.tabs.components()
        ],
      ),
      # Animação de Carregamento
      ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
          self.loading
        ]
      ),
      self.indicador.view
    )
    page.scroll = "always"
    
    
  def send_command(self, prompt:str, e):
    # Mostra a animação de carregamento
    self.clean_data()
    self.loading.visible = True
    self.page.update()

    indicadores = json.load(open(f'Q:/GROUPS/BR_SC_JGS_WM_LOGISTICA/PCP/PPC_AI_Procedures/ppc_secretary/indicadores/{self.tabs.tab_selecionada}.json', 'r', encoding='utf-8'))
    for indicador in indicadores:
      if indicador['Name'] == prompt and indicador['Status'] != 'Realizado':
        self.indicador.finish_button.visible = True

    self.indicador_atual = prompt
    topicos, resumo = self.ia.send_message(prompt)
    self.indicador.tasks_view.controls.clear() 

    for topico in topicos:
        if re.search(r'https?://(?:www\.)?[\w\d\-.]+\.[\w]{2,6}(?:/[\w\d\.\/\-_%&?=\+]+)?', topico) or re.search(r'[A-Za-z]:(?:\\|/)(?:[^\\/]+(?:\\|/))*[^\\/]+', topico)  or re.search(r'[\w\.-]+@[\w\.-]+\.\w+', topico):
          links = re.findall(r'https?://(?:www\.)?[\w\d\-.]+\.[\w]{2,6}(?:/[\w\d\.\/\-_%&?=\+]+)?', topico)
          pastas = re.findall(r'[A-Za-z]:(?:\\|/)(?:[^\\/]+(?:\\|/))*[^\\/]+', topico)
          emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', topico)
          found = ''
          self.button_img = ft.Image(src="images/copiar-arquivo.png", width=40)

          if emails:
            found = 'Enviar E-mail'
            self.button_img = ft.Image(src="images/outlook.png", width=40)

          elif links:
            found = 'Abrir Link da Web'
            self.button_img = ft.Image(src="images/web.png", width=40)

          elif pastas:
            found = 'Abrir Arquivo da Rede'
            self.button_img = ft.Image(src="images/abrir.png", width=40)
             
          def copy_topico(e, texto=topico):
              links = re.findall(r'https?://(?:www\.)?[\w\d\-.]+\.[\w]{2,6}(?:/[\w\d\.\/\-_%&?=\+]+)?', texto)
              pastas = re.findall(r'[A-Za-z]:(?:\\|/)(?:[^\\/]+(?:\\|/))*[^\\/]+', texto)
              emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', texto)

              if emails:
                parts = ''.join(texto).split('|')
                subject = ''
                to = ''
                body = ''
                cc = ''
                bcc = ''
                attachments = None
                for part in parts:
                   if part.strip().startswith('Title:'): subject = part.replace('Title:','')
                   if part.strip().startswith('To:'): to = part.replace('To:','')
                   if part.strip().startswith('Body:'): body = part.replace('Body:','')
                   if part.strip().startswith('Copy:'): cc = part.replace('Copy:','')
                   if part.strip().startswith('CCo:'): bcc = part.replace('CCo:','')
                   if part.strip().startswith('Attachments:'): attachments = part.replace('Attachments:','').split(';')

                pythoncom.CoInitialize()
                Outlook().send_email(subject,to,body,cc,bcc,attachments)
                pyperclip.copy(''.join(emails))

              elif links:
                  pyperclip.copy(links[0])
                  os.startfile(links[0])

              elif pastas:
                  pyperclip.copy(pastas[0])
                  os.startfile(pastas[0])

          row = ft.Row(
              controls=[
                  ft.Checkbox(),
                  ft.Text(topico,size=15,text_align=ft.TextAlign.LEFT,expand=True),
                  ft.ElevatedButton(
                    content=self.button_img,
                    on_click=copy_topico,  # Adiciona evento de clique
                    style=ft.ButtonStyle(
                        padding=ft.padding.all(0),  # Remove o padding
                        elevation=0,                # Remove a sombra
                        bgcolor=ft.colors.TRANSPARENT,   # Define o fundo como transparente
                    ),
                    tooltip=f"{found}"  # Definir o texto do tooltip
                  )
              ],
          )
        else:
            # Se não é um link, cria a linha sem o botão
            row = ft.Row(
                controls=[
                    ft.Checkbox(),
                    ft.Text(topico, size=15, text_align=ft.TextAlign.LEFT, expand=True)
                ]
            )

        self.indicador.tasks_view.controls.append(
          ft.Column(
          controls=[
            ft.Divider(height=1),
            row,
          ]))

    self.indicador.indicador_atual.value = f"{self.app_text.get('procedure_description')} {prompt}:\n{resumo}"
    self.loading.visible = False
    self.page.update()  # Atualiza a interface

  #TERMINAR LIMPEZA!!!!
  def clean_data(self):
    run_all()
    self.indicador.tasks_view.controls.clear() 
    self.indicador.finish_button.visible = False
    self.indicador.indicador_atual.value = ""
    self.page.update()  # Atualiza a interface


  def finish(self, e):
    if self.indicador_atual != '':
      indicadores = json.load(open(f'Q:/GROUPS/BR_SC_JGS_WM_LOGISTICA/PCP/PPC_AI_Procedures/ppc_secretary/indicadores/{self.tabs.tab_selecionada}.json', 'r', encoding='utf-8'))
      for indicador in indicadores:
        if indicador['Name'] == self.indicador_atual:
          indicador['Status'] = 'Realizado'
          indicador['LastUpdate'] = str(date.today())
      json.dump(indicadores, open(f'Q:/GROUPS/BR_SC_JGS_WM_LOGISTICA/PCP/PPC_AI_Procedures/ppc_secretary/indicadores/{self.tabs.tab_selecionada}.json', 'w', encoding='utf-8'), indent=4)

      self.tabs.indicadores.controls.clear()
      indicadores = json.load(open(f'Q:/GROUPS/BR_SC_JGS_WM_LOGISTICA/PCP/PPC_AI_Procedures/ppc_secretary/indicadores/{self.tabs.tab_selecionada}.json', 'r', encoding='utf-8'))
      for indicador in indicadores:
        if indicador['Status'] == 'Pendente':
            cor = '#F9EC9B'
        else:
            cor = '#BDECB6'
            
        self.tabs.indicadores.controls.append(
            self.tabs.criar_botao(indicador['Name'], cor)
        )

      self.indicador.finish_button.visible = False
      self.page.update()


if __name__ == "__main__":
  graphic = Graphic()