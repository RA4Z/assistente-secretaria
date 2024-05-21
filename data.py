from extract import Dados
import json
import os

data = Dados()
path_weekly = 'Q:/GROUPS/BR_SC_JGS_WM_LOGISTICA/PCP/Ester/Manual de Procedimentos/Indicadores Semanal'
path_monthly = 'Q:/GROUPS/BR_SC_JGS_WM_LOGISTICA/PCP/Ester/Manual de Procedimentos/Indicadores Mensal'
path_daily = 'Q:/GROUPS/BR_SC_JGS_WM_LOGISTICA/PCP/Ester/Manual de Procedimentos/Diário'
path_procedures = 'Q:/GROUPS/BR_SC_JGS_WM_LOGISTICA/PCP/PPC_AI_Procedures/general_procedures'
path_rules = 'Q:/GROUPS/BR_SC_JGS_WM_LOGISTICA/PCP/PPC_AI_Procedures/rules'

agendaPCP = json.load(open('agenda.json', 'r', encoding='utf-8'))

paths = [path_daily, path_weekly, path_monthly, path_procedures, path_rules]
historico = []

#INSERIR INFORMAÇÕES DA AGENDA DO PCP, CRIADA PELA MARGUIT
for seq in agendaPCP:
    historico.append({
        "role": "user",
        "parts": [
            f"Agenda PCP Sequência {seq['SEQ']}:"
        ]
    })
    historico.append({
        "role": "model",
        "parts": [
            f"\nSequência: {seq['SEQ']}\n{seq['REFERÊNCIA']}\nDescrição: {seq['DESCRIÇÃO']}\nUtilidade: {seq['UTILIDADE']}"+ 
            (f"\nDetalhes: {seq['DETALHES']}" if 'DETALHES' in seq else "")
        ]
    })

#INSERIR PROCEDIMENTOS E DOCUMENTOS WORD
for path in paths:
    for filename in os.listdir(path):
        if filename.endswith(".docx"):
            historico.append({
                "role": "user",
                "parts": [
                    f"Procedimento em extenso para {filename}"
                ]
            })
            historico.append({
                "role": "model",
                "parts": [
                    data.extrair_procedimento(f'{path}/{filename}'),
                ]
            })


