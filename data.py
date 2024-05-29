from extract import Dados
from rotinas import run_all
import json
import os

run_all()

data = Dados()
path_daily = 'Q:\GROUPS\BR_SC_JGS_WM_LOGISTICA\PCP\PPC_AI_Procedures\ppc_secretary\daily'
path_weekly = 'Q:\GROUPS\BR_SC_JGS_WM_LOGISTICA\PCP\PPC_AI_Procedures\ppc_secretary\weekly'
path_monthly = 'Q:\GROUPS\BR_SC_JGS_WM_LOGISTICA\PCP\PPC_AI_Procedures\ppc_secretary\monthly'
# path_procedures = 'Q:/GROUPS/BR_SC_JGS_WM_LOGISTICA/PCP/PPC_AI_Procedures/general_procedures'
# path_rules = 'Q:/GROUPS/BR_SC_JGS_WM_LOGISTICA/PCP/PPC_AI_Procedures/rules'

# agendaPCP = json.load(open('agenda.json', 'r', encoding='utf-8'))

paths = [path_daily, path_weekly, path_monthly]
historico = []

#INSERIR INFORMAÇÕES DA AGENDA DO PCP, CRIADA PELA MARGUIT
# for seq in agendaPCP:
#     historico.append({
#         "role": "user",
#         "parts": [
#             f"Agenda PCP Sequência {seq['SEQ']}:"
#         ]
#     })
#     historico.append({
#         "role": "model",
#         "parts": [
#             f"\nSequência: {seq['SEQ']}\n{seq['REFERÊNCIA']}\nDescrição: {seq['DESCRIÇÃO']}\nUtilidade: {seq['UTILIDADE']}"+ 
#             (f"\nDetalhes: {seq['DETALHES']}" if 'DETALHES' in seq else "")
#         ]
#     })

#INSERIR PROCEDIMENTOS E DOCUMENTOS WORD
for path in paths:
    for filename in os.listdir(path):
        if filename.endswith(".docx"):
            historico.append({
                "role": "user",
                "parts": [
                    f"Procedimento em extenso para o indicador {filename.replace('.docx','')}"
                ]
            })
            historico.append({
                "role": "model",
                "parts": [
                    data.extrair_procedimento(f'{path}/{filename}'),
                ]
            })


#VERIFICAR STATUS DE INDICADORES
#INDICADORES DIÁRIOS
diarios = json.load(open('Q:/GROUPS/BR_SC_JGS_WM_LOGISTICA/PCP/PPC_AI_Procedures/ppc_secretary/indicadores/diarios.json', 'r', encoding='utf-8'))
historico.append({
    "role": "user",
    "parts": [
        f"Status atual de todos os indicadores diários da secretária"
    ]
})
historico.append({
    "role": "model",
    "parts": [
        str(diarios),
    ]
})

#INDICADORES SEMANAIS
semanais = json.load(open('Q:/GROUPS/BR_SC_JGS_WM_LOGISTICA/PCP/PPC_AI_Procedures/ppc_secretary/indicadores/semanais.json', 'r', encoding='utf-8'))
historico.append({
    "role": "user",
    "parts": [
        f"Status atual de todos os indicadores semanais da secretária"
    ]
})
historico.append({
    "role": "model",
    "parts": [
        str(semanais),
    ]
})

#INDICADORES MENSAIS
mensais = json.load(open('Q:/GROUPS/BR_SC_JGS_WM_LOGISTICA/PCP/PPC_AI_Procedures/ppc_secretary/indicadores/mensais.json', 'r', encoding='utf-8'))
historico.append({
    "role": "user",
    "parts": [
        f"Status atual de todos os indicadores mensais da secretária"
    ]
})
historico.append({
    "role": "model",
    "parts": [
        str(mensais),
    ]
})
