import flet as ft
import json
import sys
import os
config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(config_dir)

class Graphic():
  def __init__(self):
    self.app_text = json.load(open(f'pages/text.json', 'r', encoding='utf-8'))


  def main(self, page: ft.Page):
    page.title = self.app_text.get('window_title')
    page.add(
      ft.Text(self.app_text.get('main_title'), size=24, text_align=ft.TextAlign.CENTER),
      ft.ElevatedButton(
        text="Clique aqui",
        on_click=lambda e: page.add(ft.Text("Você clicou no botão!", size=20))
      ),
    )

graphic = Graphic()

if __name__ == "__main__":
  ft.app(target=graphic.main)