from server import app
from flask import render_template, request

import requests as Req

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        senha = request.form['senha']
        
        url = "https://ivjbikerepair.herokuapp.com/loginOficina"
        login = {'email': email, 'senha': senha}
        retorno = Req.api.post(url, json=login).json()
        dados = retorno['dados']
        status = retorno['status']

        if(status == "OK"):
            return render_template('Dashboard.html',oficina=dados)
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
        horarioFuncionamento = request.form['horarioFuncionamento']

        url = "https://ivjbikerepair.herokuapp.com/cadastrarOficina"
        cadastro = {'nome': nome, 'email': email, 'senha': senha, 'cpfCnpj': cpfCnpj, 'horarioFuncionamento': horarioFuncionamento}
        retorno = Req.api.post(url, json=cadastro).json()
        dados = retorno['dados']
        status = retorno['status']

        print(cadastro)

        if(status == "OK"):
            
            latitude = float(request.form['latitude'])
            longitude = float(request.form['longitude'])
            cep = int(request.form['cep'])
            numero = int(request.form['numero'])

            url2 = "https://ivjbikerepair.herokuapp.com/cadastrarEndereco"
            endereco = {"latitude":latitude, "longitude":longitude, "cep":cep, "numero":numero}
            oficina2 = {"email": email}
            json = {"endereco": endereco, "oficina": oficina2}

            retornoE = Req.api.post(url2, json=json).json()
            dadosE = retornoE['dados']
            statusE = retornoE['status']

            if(statusE == "OK"):
                return render_template('login.html')
            else:
                print("endereco")
                return render_template('error.html')
        else:
            print("cadastro")
            return render_template('error.html')
    
    
    nome = request.form['nome']
    print(nome)
    

@app.route("/cadastrarProduto")
def cadastrarProduto():
    return render_template('Dashboard.html',oficina=dados)

@app.route("/dashboard")
def dashboard(email, senha):
    return render_template('Dashboard.html',oficina=dados)


