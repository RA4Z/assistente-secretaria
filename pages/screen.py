import flet as ft
import json
import sys
import os
from datetime import date
  
config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(config_dir)

from gemini import GeminiAI
from components.Aba import Aba
from components.Indicador import Indicador

class Graphic(ft.UserControl):
  def __init__(self):
    self.app_text = json.load(open(f'pages/text.json', 'r', encoding='utf-8'))
    self.ia = GeminiAI()
    ft.app(target=self.main)


  def main(self, page: ft.Page):
    self.page = page  # Armazena a referência para a página
    page.title = self.app_text.get('window_title')
    self.indicador_atual = ''
    self.tabs = Aba(page, self.send_command, self.clean_data)
    self.indicador = Indicador(page, self.finish)

    page.add(
      ft.Text(self.app_text.get('main_title'), size=24, text_align=ft.TextAlign.CENTER, weight='bold'),
      ft.Container(
        height=15
      ),
      ft.Row(
        controls=[
          self.tabs.components()
        ],
      ),
      self.indicador.view
    )
    page.scroll = "always"
    
    
  def send_command(self, prompt:str, e):
    self.indicador.finish_button.visible = True
    self.indicador_atual = prompt
    topicos, resumo = self.ia.send_message(prompt)
    self.indicador.tasks_view.controls.clear() 

    for topico in topicos:
        self.indicador.tasks_view.controls.append(
          ft.Row(
              controls=[
                  ft.Checkbox(),
                  ft.Text(topico,size=15,text_align=ft.TextAlign.LEFT,expand=True),
              ],
          )
        )

    self.indicador.indicador_atual.value = f"{self.app_text.get('procedure_description')} {prompt}:\n{resumo}"
    self.page.update()  # Atualiza a interface

  #TERMINAR LIMPEZA!!!!
  def clean_data(self):
    self.indicador.tasks_view.controls.clear() 
    self.indicador.finish_button.visible = False
    self.indicador.indicador_atual.value = ""
    self.page.update()  # Atualiza a interface

  def finish(self, e):
    if self.indicador_atual != '':
      indicadores = json.load(open(f'data/{self.tabs.tab_selecionada}.json', 'r', encoding='utf-8'))
      for indicador in indicadores:
        if indicador['Name'] == self.indicador_atual:
          indicador['Status'] = 'Realizado'
          indicador['LastUpdate'] = str(date.today())
      json.dump(indicadores, open(f'data/{self.tabs.tab_selecionada}.json', 'w', encoding='utf-8'), indent=4)

      self.tabs.indicadores.controls.clear()
      indicadores = json.load(open(f'data/{self.tabs.tab_selecionada}.json', 'r', encoding='utf-8'))
      for indicador in indicadores:
        if indicador['Status'] == 'Pendente':
            cor = '#F9EC9B'
        else:
            cor = '#BDECB6'
            
        self.tabs.indicadores.controls.append(
            self.tabs.criar_botao(indicador['Name'], cor)
        )

      self.page.update()


if __name__ == "__main__":
  graphic = Graphic()