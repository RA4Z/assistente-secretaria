import flet as ft
import json
import sys
import os

config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(config_dir)

from components.Aba import Aba
from gemini import GeminiAI

class Graphic(ft.UserControl):
  def __init__(self):
    self.app_text = json.load(open(f'pages/text.json', 'r', encoding='utf-8'))
    self.ia = GeminiAI()
    self.styles()
    ft.app(target=self.main)


  def main(self, page: ft.Page):
    self.page = page  # Armazena a referência para a página
    page.title = self.app_text.get('window_title')

    page.add(
      ft.Text(self.app_text.get('main_title'), size=24, text_align=ft.TextAlign.CENTER),
      ft.Row(
          controls=[
              Aba(page).components()
          ],
      ),
      self.view,
    )
    page.scroll = "always"
    

  def styles(self):
    self.indicador_atual = ft.Text("", size=15, text_align=ft.TextAlign.CENTER, expand=True)
    self.tasks_view = ft.Column(width=800)

    self.finish_button = ft.ElevatedButton(
        text=self.app_text.get('finish_button'),
        height=50,
        on_click=lambda e: self.finish(e),
        visible=False
    )

    self.view=ft.Column(
      controls=[
          ft.Row(
              controls=[self.indicador_atual,self.finish_button],
              alignment=ft.MainAxisAlignment.CENTER,
          ), 
          self.tasks_view,
      ],
    )


  def send_command(self, e):
    if self.new_task.value != '':
      self.finish_button.visible = True
      topicos, resumo = self.ia.send_message(self.new_task.value)
      self.tasks_view.controls.clear() 

      for topico in topicos:
        self.tasks_view.controls.append(ft.Checkbox(label=topico))

      self.indicador_atual.value = f"{self.app_text.get('procedure_description')} {self.new_task.value}:\n{resumo}"
      self.new_task.value = ""
      self.page.update()  # Atualiza a interface


  def finish(self, e):
    pass


if __name__ == "__main__":
  graphic = Graphic()