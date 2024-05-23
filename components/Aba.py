import flet as ft
import json
import sys
import os

config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(config_dir)


class Aba(ft.UserControl):
    def __init__(self, page: ft.Page, on_click):
        self.page = page
        self.on_click = on_click
        self.prompt = ''
        self.tab_selecionada = ''
        self.indicador_atual = ft.Text("", size=20, text_align=ft.TextAlign.CENTER, width=350)
        self.indicadores = ft.Row(wrap=True, width= self.page.window_width - 350)
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
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Container(
                    height=25
                ),
                ft.Row (
                    controls=[self.indicador_atual, self.indicadores],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Container(
                    height=25
                ),
            ]
        )
  

    def select_tab(self, selected:str, e):
        self.indicador_atual.value = f'Visualizando indicadores {selected}'
        self.tab_selecionada = selected
        indicadores = json.load(open(f'data/{selected}.json', 'r', encoding='utf-8'))
        self.indicadores.controls.clear()
        for indicador in indicadores:
            if indicador['Status'] == 'Pendente':
                cor = '#F9EC9B'
            else:
                cor = '#BDECB6'
                
            self.indicadores.controls.append(
                self.criar_botao(indicador['Name'], cor)
            )

        self.page.update()


    def criar_botao(self, nome_indicador, cor):
        def on_click(e):
            self.on_click(nome_indicador, e)
        return ft.ElevatedButton(
            text=nome_indicador,
            height=50,
            bgcolor=cor,
            on_click=on_click
        )

    def pesquisar_indicador(self, indicador:str, e):
        self.prompt = indicador
    