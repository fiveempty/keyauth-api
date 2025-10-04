from flask import Flask, request, jsonify
import requests
import random
import string

app = Flask(__name__)

# sua chave de vendedor do KeyAuth
SELLER_KEY = "a3481628d51b53cf564c8092e2c2ab14"

# o nome da sub que você criou no painel do KeyAuth
SUBSCRIPTION = "MeuPlano"  

# função pra gerar user/senha automáticos
def gerar_user_pass(comprador):
    username = comprador + "_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return username, password

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    comprador = data.get("comprador", "cliente")   # depende do OwliVery
    produto = data.get("produto", "default")

    # gera login e senha
    username, password = gerar_user_pass(comprador)

    # chamada pra API do KeyAuth
    url = "https://keyauth.win/api/seller/"
    params = {
        "sellerkey": SELLER_KEY,
        "type": "adduser",
        "user": username,
        "pass": password,
        "sub": SUBSCRIPTION,
        "expiry": "30"   # validade em dias
    }

    r = requests.get(url, params=params)

    if "success" in r.text.lower():
        return jsonify({
            "status": "ok",
            "username": username,
            "password": password,
            "mensagem": "Usuário criado no KeyAuth com sucesso!"
        })
    else:
        return jsonify({
            "status": "erro",
            "resposta": r.text
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
