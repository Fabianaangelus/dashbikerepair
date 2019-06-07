from model import Util
from server import app
from flask import render_template, redirect, request


@app.route("/", methods=['GET']) 
def index():
    oficinas = Util.getRequest("listarOficinas")['dados']
    
    oficinasAgrupadas = []
    count = 0
    grupo3 = []
    for oficina in oficinas:
        if(len(grupo3) == 3):
            grupo3 = []

        oficina["teste"] = True
        grupo3.append(oficina)

        if(count == 2):
            print(grupo3)
            oficinasAgrupadas.append(grupo3)
            count = 0

        count += 1

    return render_template('index.html', oficinas=oficinasAgrupadas)

@app.route("/oficina/<id>", methods=['GET']) 
def exibirOficina(id):
    oficina = {'id': int(id)}
    retornoOficina = Util.postRequest("buscarOficina", oficina)
    print("###########")
    print(retornoOficina)
    return render_template('oficina.html', oficina=retornoOficina)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        senha = request.form['senha']

        if(email == "admin" and senha == "admin"):
            return redirect("/admin")

        login = {'email': email, 'senha': senha}
        retornoLogin = Util.postRequest("loginOficina", login)
        statusLogin = retornoLogin['status']
        Util.oficinaEscolhida = retornoLogin['dados']
        
        print(statusLogin)

        if(statusLogin == "OK"):
            return redirect("/dashboard")
        else:
            return redirect("/erro")

@app.route("/dashboard", methods=['GET'])
def dashboard(): 
    produtos = {"email": Util.oficinaEscolhida['email']}
    retornoProdutos = Util.postRequest("listarProdutos", produtos)
    Util.produtos = retornoProdutos['dados']

    ordemServico = {"email": Util.oficinaEscolhida['email']}
    retornoOrdemServico = Util.postRequest("listarOrdemServicoOficina", ordemServico)
    Util.ordemServicos = retornoOrdemServico['dados']

    datasOs = []
    meses = []
    quantidade = []

    for os in Util.ordemServicos:
        valor = str(os['data'])
        data = ""
        if(len(valor) == 8):
            data = valor[2:]
        else:
            data = valor[1:]

        mes = data[:2]
        ano = data[2:]

        datasOs.append(mes+"/"+ano)

    for os in datasOs:
        adiciona = True
        for mes in meses:
            if(mes == os):
                adiciona = False

        if(adiciona):
            meses.append(os)
            quantidade.append(datasOs.count(os))


    print(meses)
    print(quantidade)


    chats = {"id" :Util.oficinaEscolhida["id"],"valor" :1}
    retornoChats = Util.postRequest("retornaChat", chats)
    Util.chats = retornoChats['dados']

    return render_template('Dashboard.html',    oficina=Util.oficinaEscolhida, 
                                                produtos=Util.produtos, 
                                                ordemServicos=Util.ordemServicos,
                                                chats=Util.chats,
                                                mensagens=Util.mensagens,
                                                label=str(meses),
                                                valores=str(quantidade) )       

@app.route("/cadastrarOficina", methods=['GET', 'POST'])
def cadastrarOficina():
    if request.method == 'GET':
        return render_template('cadastrarOficina.html')
    else:
        nome =  Util.persistirDados(request.form['nome'], str, False)
        email = Util.persistirDados(request.form['email'], str, False)
        senha = Util.persistirDados(request.form['senha'], str, False)
        cpfCnpj = Util.persistirDados(request.form['cpfCnpj'], str, False)

        inicio = Util.persistirDados(request.form['inicio'], str, False)
        fim = Util.persistirDados(request.form['fim'], str, False)

        if(inicio and fim):
            horarioFuncionamento = inicio+"-"+fim
        else:
            horarioFuncionamento = False


        status = "NOK"        

        if(nome and email and senha and cpfCnpj and horarioFuncionamento):
            cadastro = {'nome': nome, 'email': email, 'senha': senha, 'cpfCnpj': cpfCnpj, 'horarioFuncionamento': horarioFuncionamento}
            retorno = Util.postRequest("cadastrarOficina", cadastro)
            status = retorno['status']

        if(status == "OK"):

            latitude = ""
            longitude = ""
            cep = ""
            numero = ""

            statusE = ""

            try:
                latitude = Util.persistirDados(float(request.form['latitude'].replace(",",".")), float, True)
                longitude = Util.persistirDados(float(request.form['longitude'].replace(",",".")), float, True)
                cep = Util.persistirDados(int(request.form['cep'].replace("-","")), int, True)
                numero = Util.persistirDados(int(request.form['numero']), int, True)

                statusE = "NOK"

                if(latitude and longitude and cep and numero):
                    endereco = {"latitude":latitude, "longitude":longitude, "cep":cep, "numero":numero}
                    oficina2 = {"email": email}
                    json = {"endereco": endereco, "oficina": oficina2}
                    retornoE = Util.postRequest("cadastrarEndereco", json)
                    statusE = retornoE['status']
                else:
                    statusE = "NOK"

            except:
                statusE = "NOK"
            
            if(statusE == "OK"):
                return render_template('login.html')
            else:
                return redirect("/erro")
        else:
            return redirect("/erro")
 
@app.route("/editarOficina", methods=['GET', 'POST'])
def editarOficina():
    if request.method == 'GET':
        horario = Util.oficinaEscolhida['horarioFuncionamento'].split("-")
        inicio = horario[0]
        fim = horario[1]
        return render_template('editarOficina.html', oficina=Util.oficinaEscolhida, inicio=inicio, fim=fim)
    else:
        descricao = Util.persistirDados(request.form['descricao'], str, False)

        inicio = Util.persistirDados(request.form['inicio'], str, False)
        fim = Util.persistirDados(request.form['fim'], str, False)

        if(inicio and fim):
            horarioFuncionamento = inicio+"-"+fim
        else:
            horarioFuncionamento = False

        if(descricao and horarioFuncionamento):
            json = {
                        "id": Util.oficinaEscolhida["id"], 
                        "senha": Util.oficinaEscolhida["senha"],
                        "descricao": descricao,
                        "avaliacaoTotal": Util.oficinaEscolhida["avaliacaoTotal"],
                        "qntOrcamentosAtendidos": Util.oficinaEscolhida["qntOrcamentosAtendidos"],
                        "qntOrcamentosRejeitados": Util.oficinaEscolhida["qntOrcamentosRejeitados"],
                        "qntReboquesAtendidos": Util.oficinaEscolhida["qntReboquesAtendidos"],
                        "qntReboquesRejeitados": Util.oficinaEscolhida["qntReboquesRejeitados"],
                        "horarioFuncionamento": horarioFuncionamento
                    }

            Util.postRequest("alterarOficina", json)
            return render_template('editarOficina.html', oficina=Util.oficinaEscolhida, inicio=inicio, fim=fim)
        else:
            return redirect("/erro")

@app.route("/alterarSenha", methods=['POST'])
def alterarSenha():
    antiga = Util.persistirDados(request.form['antiga'], str, False)
    nova = Util.persistirDados(request.form['nova'], str, False)

    horario = Util.oficinaEscolhida['horarioFuncionamento'].split("-")
    inicio = horario[0]
    fim = horario[1]

    if( (nova and antiga) and (antiga == Util.oficinaEscolhida['senha']) ):
        json = {
                    "id": Util.oficinaEscolhida["id"], 
                    "senha": nova,
                    "descricao": Util.oficinaEscolhida["descricao"],
                    "avaliacaoTotal": Util.oficinaEscolhida["avaliacaoTotal"],
                    "qntOrcamentosAtendidos": Util.oficinaEscolhida["qntOrcamentosAtendidos"],
                    "qntOrcamentosRejeitados": Util.oficinaEscolhida["qntOrcamentosRejeitados"],
                    "qntReboquesAtendidos": Util.oficinaEscolhida["qntReboquesAtendidos"],
                    "qntReboquesRejeitados": Util.oficinaEscolhida["qntReboquesRejeitados"],
                    "horarioFuncionamento": Util.oficinaEscolhida["horarioFuncionamento"]
                }

        Util.postRequest("alterarOficina", json)
        return render_template('editarOficina.html', oficina=Util.oficinaEscolhida, inicio=inicio, fim=fim)
    else:
        return redirect("/erro")

@app.route("/cadastrarProduto", methods=['GET', 'POST'])
def cadastrarProduto():
    if request.method == 'GET':
        return render_template('cadastrarProduto.html', oficina=Util.oficinaEscolhida)
    else:
        nome = request.form['nome']
        preco = float(request.form['preco'])
        descricao = request.form['descricao']
        categoria = request.form['categoria']
        precoCancelamento = float(request.form['precoCancelamento'])

        produto = {"nome": nome, "preco": preco, "descricao": descricao, "categoria": categoria, "precoCancelamento": precoCancelamento}
        oficina = {"email": Util.oficinaEscolhida['email']}

        json = {"produto": produto, "oficina": oficina}

        Util.postRequest("cadastrarProduto",json)

        return redirect("/dashboard")

@app.route("/dashboard/chat/<id>", methods=['GET'])
def dashboardChat(id):
    json = {"id": int(id), "valor": 1}
    retornoMsgChat = Util.postRequest("exibirMensagensChat", json)
    Util.mensagens = retornoMsgChat['dados']
    statusMsgChat = retornoMsgChat['status']
    Util.chatEscolhido = id
    return redirect("/dashboard")

@app.route("/enviarMensagem", methods=['POST'])
def enviarMensagem():
    mensagem = antiga = Util.persistirDados(request.form['message'], str, False)
    if(mensagem):
        mensagemJson = {"texto": mensagem}
        chatJson = {"id": Util.chatEscolhido}
        chaveJson = {"valor": 1}
        json = {"mensagem": mensagemJson, "chat": chatJson, "chave": chaveJson}
        retorno = Util.postRequest("criarMensagemChat", json)
        status = retorno["status"]
        
        if(status == "OK"):
            caminho = "/dashboard/chat/"+Util.chatEscolhido
            return redirect(caminho)
        else:
            return redirect("/erro")
    else:
        return redirect("/erro")

@app.route("/admin", methods=['GET'])
def painelAdmin():
    clientes = Util.getRequest("listarClientes")['dados']
    oficinas = Util.getRequest("listarOficinas")['dados']

    efetuados = 0
    rejeitados = 0
    users = len(clientes)
    of = len(oficinas)

    for dados in oficinas:
        efetuados = efetuados + dados["qntOrcamentosAtendidos"]
        efetuados = efetuados + dados["qntReboquesAtendidos"]

        rejeitados = rejeitados + dados["qntOrcamentosRejeitados"]
        rejeitados = rejeitados + dados["qntReboquesRejeitados"]

    return render_template('painelAdmin.html',  efetuados=efetuados,
                                                rejeitados=rejeitados,
                                                usuarios=users,
                                                oficinas=of)

@app.route("/erro", methods=['GET'])
def telaError():
    dados = ""
    return render_template('error.html',oficina=dados)

