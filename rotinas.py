import json
from datetime import date

def diarios():
    indicadores = json.load(open('data/diarios.json', 'r', encoding='utf-8'))
    for indicador in indicadores:
        if indicador['LastUpdate'] == str(date.today()):
            indicador['Status'] = "Realizado"
        else:
            indicador['Status'] = "Pendente"

    json.dump(indicadores, open('data/diarios.json', 'w', encoding='utf-8'), indent=4)

    
