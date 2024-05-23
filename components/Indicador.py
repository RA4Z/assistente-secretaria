import flet as ft
import json
import sys
import os

config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(config_dir)

class Indicador(ft.UserControl):
    def __init__(self, page: ft.Page, on_click):
        self.on_click = on_click
        self.app_text = json.load(open(f'pages/text.json', 'r', encoding='utf-8'))
        self.page = page
        self.styles()
    
    def styles(self):
        self.indicador_atual = ft.Text("", size=15, text_align=ft.TextAlign.CENTER, width=self.page.window_width - 400)
        self.tasks_view = ft.Column(width=800)

        self.finish_button = ft.ElevatedButton(
            text=self.app_text.get('finish_button'),
            height=50,
            on_click=lambda e: self.on_click(e),
            visible=False
        )

        self.view=ft.Column(
            controls=[
                ft.Row(
                    controls=[self.indicador_atual,self.finish_button],
                    alignment=ft.MainAxisAlignment.CENTER,
                ), 
                ft.Container(
                    height=25
                ),
                self.tasks_view,
            ],
        )

