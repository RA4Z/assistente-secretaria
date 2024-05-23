import flet as ft
import json
import sys
import os

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
    self.tabs = Aba(page, self.send_command)
    self.indicador = Indicador(page)

    page.add(
      ft.Text(self.app_text.get('main_title'), size=24, text_align=ft.TextAlign.CENTER),
      ft.Container(
          height=15
      ),
      ft.Row(
          controls=[
            self.tabs.components()
          ],
      ),
      ft.Row(
          controls=[
            self.indicador.view
          ]
      ),
    )
    page.scroll = "always"
    
    
  def send_command(self, prompt:str, e):
    self.indicador.finish_button.visible = True
    topicos, resumo = self.ia.send_message(prompt)
    self.indicador.tasks_view.controls.clear() 

    for topico in topicos:
        self.indicador.tasks_view.controls.append(ft.Checkbox(label=topico))

    self.indicador.indicador_atual.value = f"{self.app_text.get('procedure_description')} {prompt}:\n{resumo}"
    self.page.update()  # Atualiza a interface


  def finish(self, e):
      pass


if __name__ == "__main__":
  graphic = Graphic()