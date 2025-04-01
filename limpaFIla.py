import requests 
import json
import time

with open("request_data.json", "r", encoding="utf-8") as arquivo:
    dadosRequest = json.load(arquivo)

departamentsRequest = requests.get("https://api.tomticket.com/v2.0/department/list?show_nested_items=0", headers={"Authorization": dadosRequest["Authorization"]})
departamentsRequestJson = departamentsRequest.json()
#print(json.dumps(departamentsRequestJson, indent=4, ensure_ascii=False))
#print(departamentsRequestJson["data"][0])

##Busca o ID do departamento Sistema
for departamento in departamentsRequestJson["data"]:
    if departamento["name"] == "Sistema" : idDepartamento = departamento["id"]

categoriaRequest = requests.get(f"https://api.tomticket.com/v2.0/department/category/list?department_id={idDepartamento}", headers={"Authorization": dadosRequest["Authorization"]})
categoriaRequestJson = categoriaRequest.json()
##print(json.dumps(categoriaRequestJson, indent=4, ensure_ascii="utf-8"))

##Busca o ID da categoria Problema 
for categoria in categoriaRequestJson["data"]:
    if categoria["name"] == "AUTO-CHECKLIST": idCategoria = categoria["id"]
##print(idCategoria)

# Consulta os chamdados de acordo com filtro
consultaChamados = requests.get(f"https://api.tomticket.com/v2.0/ticket/list?page=1&customer_id={dadosRequest["customer_id"]}&customer_type_id={dadosRequest["customer_id_type"]}&situation=0,1,2,3,6,7,8,9&department_id={idDepartamento}", headers={"Authorization": dadosRequest["Authorization"]})
consultaChamadosJson = consultaChamados.json()
# print(json.dumps(consultaChamadosJson, indent=4, ensure_ascii="utf-8"))

# Valida se há chamados e caso haja questionar se deseja finalizar
if consultaChamadosJson["data"]:
    print(f"Foram encontrados {len(consultaChamadosJson["data"])} chamados")
    chamadosSC2 = []
    # Filtra as informações necessárias
    for chamado in consultaChamadosJson["data"]:
        chamadosSC2.append({"protocol": chamado["protocol"], "idChamado": chamado["id"], "situation": chamado["situation"]["description"], "subject": chamado["subject"]})
    ##Escreve os chamados buscados para finalização
    for chamado in chamadosSC2:
        print(f"Chamado: {chamado["protocol"]}, Situacao: {chamado["situation"]}, Subject: {chamado["subject"]}")
    resp = input("Deseja finalizar os chamados? S/N")
    if resp == "S":
        for chamado in chamadosSC2: 
            vinculacaoAtendente = requests.post("https://api.tomticket.com/v2.0/ticket/operator/link", headers={"Authorization": dadosRequest["Authorization"]}, data={"ticket_id": chamado["idChamado"], "operator_id": "afb3d8f991a888a24a216fce55aafb24"})
            vinculacaoAtendenteJson = vinculacaoAtendente.json()
            if(vinculacaoAtendenteJson["error"] ==  False): print(f"Chamado {chamado["idChamado"]} vinculado com sucesso!")
            else: print(vinculacaoAtendenteJson, chamado["idChamado"])
            time.sleep(0.5)
            finalizacaoChamado = requests.post(dadosRequest["urlFinalization"], headers={"Authorization": dadosRequest["Authorization"]}, data={"ticket_id": chamado["idChamado"], "message": "Chamado finalizado via API"})
            finalizacaoChamadoJson = finalizacaoChamado.json()
            if(finalizacaoChamadoJson["error"] == False): print(f"Chamado {chamado["idChamado"]} finalizado com sucesso!")
            else: print(finalizacaoChamadoJson)
            time.sleep(0.5)
else: print("Não foram encotrados chamados ")

##Busca o ID dos atendentes
##operatorResquest = requests.get(f"https://api.tomticket.com/v2.0/department/operator/list?department_id={idDepartamento}", headers={"Authorization": dadosRequest["Authorization"]})
##operatorResquestJson = operatorResquest.json()
##print(json.dumps(operatorResquestJson, indent=4, ensure_ascii="utf-8"))

##Teste de finalização de chamado 
##retorno = requests.post(dadosRequest["urlFinalization"], headers={"Authorization": dadosRequest["Authorization"]}, data={"ticket_id": "3bcdd870031fcffeda49dbee072dfa12", "message": "Chamado finalizado via API"})
##retornoJson = retorno.json()
##print(json.dumps(retornoJson, indent=4, ensure_ascii="utf-8"))

