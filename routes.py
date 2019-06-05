from server import app
from flask import render_template, request

import requests as Req

from model import Util

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        senha = request.form['senha']

        login = {'email': email, 'senha': senha}
        retornoLogin = postRequest("loginOficina", login)
        statusLogin = retornoLogin['status']
        Util.oficinaEscolhida = retornoLogin['dados']
        
        if(statusLogin == "OK"):

            produtos = {"email": email}
            retornoProdutos = postRequest("listarProdutos", produtos)
            Util.produtos = retornoProdutos['dados']


            ordemServico = {"email": email}
            retornoOrdemServico = postRequest("listarOrdemServicoOficina", ordemServico)
            Util.ordemServicos = retornoOrdemServico['dados']

            chats = {"id" :Util.oficinaEscolhida["id"],"valor" :1}
            retornoChats = postRequest("retornaChat", chats)
            Util.chats = retornoChats['dados']
            print(Util.chats)

            return render_template('Dashboard.html',    oficina=Util.oficinaEscolhida, 
                                                        produtos=Util.produtos, 
                                                        ordemServicos=Util.ordemServicos,
                                                        chats=Util.chats)
        else:
            return render_template('error.html',oficina=dados)
        


@app.route("/cadastrarOficina", methods=['GET', 'POST'])
def cadastrarOficina():
    if request.method == 'GET':
        return render_template('cadastrarOficina.html')
    else:
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        cpfCnpj = request.form['cpfCnpj']
        horarioFuncionamento = request.form['inicio']+"-"+request.form['fim']

        cadastro = {'nome': nome, 'email': email, 'senha': senha, 'cpfCnpj': cpfCnpj, 'horarioFuncionamento': horarioFuncionamento}
        retorno = postRequest("cadastrarOficina", cadastro)

        dados = retorno['dados']
        status = retorno['status']

        print(cadastro)

        if(status == "OK"):
            
            latitude = float(request.form['latitude'])
            longitude = float(request.form['longitude'])
            cep = int(request.form['cep'])
            numero = int(request.form['numero'])

            endereco = {"latitude":latitude, "longitude":longitude, "cep":cep, "numero":numero}
            oficina2 = {"email": email}
            
            json = {"endereco": endereco, "oficina": oficina2}
            retornoE = postRequest("cadastrarEndereco", json)

            dadosE = retornoE['dados']
            statusE = retornoE['status']

            if(statusE == "OK"):
                return render_template('login.html')
            else:
                return render_template('error.html')
        else:
            return render_template('error.html')
    

@app.route("/cadastrarProduto", methods=['GET', 'POST'])
def cadastrarProduto():
    if request.method == 'GET':
        return render_template('cadastrarProduto.html')
    else:
        nome = request.form['nome']
        preco = float(request.form['preco'])
        descricao = request.form['descricao']
        categoria = request.form['categoria']
        precoCancelamento = float(request.form['precoCancelamento'])

        produto = {"nome": nome, "preco": preco, "descricao": descricao, "categoria": categoria, "precoCancelamento": precoCancelamento}
        oficina = {"email": Util.oficinaEscolhida["email"]}

        json = {"produto": produto, "oficina": oficina}

        postRequest("cadastrarProduto",json)

        return render_template('Dashboard.html',oficina=Util.oficinaEscolhida,produtos=Util.produtos)


@app.route("/dashboard")
def dashboard(email, senha):
    return render_template('Dashboard.html',oficina=dados)



def postRequest(caminho, json):
    url = "https://ivjbikerepair.herokuapp.com/" + caminho
    resposta = Req.api.post(url, json=json).json()
    return resposta

@app.route("/painelAdmin")
def painelAdmin():
    return render_template('painelAdmin.html')



