import requests as Req

oficinaEscolhida = ""
produtos = ""
ordemServicos = ""
chats = ""
mensagens = ""
chatEscolhido = ""

def postRequest(caminho, json):
    url = "https://ivjbikerepair.herokuapp.com/" + caminho
    resposta = Req.api.post(url, json=json).json()
    return resposta

def getRequest(caminho):
    url = "https://ivjbikerepair.herokuapp.com/" + caminho
    resposta = Req.api.get(url).json()
    return resposta

def persistirDados(dado, tipo, numero):
    if(numero):
        if( isinstance(dado, tipo) ):
            return dado
        else:
            return False
    else:
        if( isinstance(dado, tipo) and (dado.strip() != "") ):
            return dado
        else:
            return False