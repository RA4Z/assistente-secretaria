import flet as ft
import json
import sys
import os

config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(config_dir)


class Aba(ft.UserControl):
    def __init__(self, page: ft.Page):
        self.page = page
        self.indicador_atual = ft.Text("Texto topzera", size=15, text_align=ft.TextAlign.CENTER)
        self.indicadores = []
        self.components()

    def components(self):
        return ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            text='Indicadores Diários',
                            height=50,
                            on_click=lambda e: self.select_tab('diarios',e)
                        ),
                        ft.ElevatedButton(
                            text='Indicadores Semanais',
                            height=50,
                            on_click=lambda e: self.select_tab('semanais',e)
                        ),
                        ft.ElevatedButton(
                            text='Indicadores Mensais',
                            height=50,
                            on_click=lambda e: self.select_tab('mensais',e)
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    controls=[self.indicador_atual],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ]
        )
  

    def select_tab(self, selected:str, e):
        self.indicador_atual.value = f'Visualizando indicadores {selected}'
        indicadores = json.load(open(f'data/{selected}.json', 'r', encoding='utf-8'))
        
        self.indicadores.clear()
        for indicador in indicadores:
            self.indicadores.append(indicador['Name'])

        print(self.indicadores)
        self.page.update()