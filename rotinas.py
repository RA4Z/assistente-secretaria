import json
from datetime import date, datetime

def diarios():
    indicadores = json.load(open('data/diarios.json', 'r', encoding='utf-8'))
    for indicador in indicadores:
        if indicador['LastUpdate'] == str(date.today()):
            indicador['Status'] = "Realizado"
        else:
            indicador['Status'] = "Pendente"

    json.dump(indicadores, open('data/diarios.json', 'w', encoding='utf-8'), indent=4)

    
def semanais():
    indicadores = json.load(open('data/semanais.json', 'r', encoding='utf-8'))
    for indicador in indicadores:
        semana_indicador = datetime.strptime(indicador['LastUpdate'],'%Y-%m-%d').isocalendar().week
        semana_atual = date.today().isocalendar().week
        if semana_indicador == semana_atual:
            indicador['Status'] = "Realizado"
        else:
            indicador['Status'] = "Pendente"
    json.dump(indicadores, open('data/semanais.json', 'w', encoding='utf-8'), indent=4)


diarios()

