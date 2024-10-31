from flask import Flask,request, jsonify,g 
from flask_socketio import SocketIO, disconnect, emit
import jwt
import json
import datetime
from functools import wraps
from flask_cors import CORS
from sugest import sugestoes
from preencher import autopreencher 
import pandas as pd
from foto import upload_to_drive
import os
from subirgoogle import confirmando
from cep import consulta_cep
from subirgoogleNovo import confirmandoNovo

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins=["http://127.0.0.1:5500"])
CORS(app)
#------------------------------------------------
with open('secret_key.json') as json_file:
    SECRET_KEY = json.load(json_file)['SECRET_KEY']
#-------------------------------------------------
usuarios = [
    {"nome": "admin", "senha": "1234"},
]

def gerar_token(nome):
    exp = datetime.datetime.utcnow() + datetime.timedelta(hours=24)

    payload = {
        'nome': nome,
        'exp': exp
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        # Verifica se o token está presente
        if not token:
            return jsonify({'message': 'Token de autorização é necessário!'}), 401

        try:
            # Remove o prefixo 'Bearer ' se houver
            token = token.replace("Bearer ", "")
            # Decodifica e valida o token
            dados = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            g.user_data = dados
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido!'}), 401

        return f(*args, **kwargs)

    return decorated

@app.route('/login', methods=['POST'])
def verificar_acesso():
    for user in usuarios:
        if user['nome'] == request.form.get("usuario"):
            if user['senha'] == request.form.get("senha"):
                return jsonify({"status": "success", "token": gerar_token(user['nome'])}) 
            else:
                return jsonify({"status": "error"})
    
    return jsonify({"status": "error"})


@app.route('/salvar_membro', methods=['POST'])
@token_required
def salvar_membro():
    user_data = g.user_data
    file = request.files['foto']
    
    if file.filename == '':
        return "Nenhum arquivo selecionado", 400

    temp_path = os.path.join("temp", file.filename)
    os.makedirs("temp", exist_ok=True)
    file.save(temp_path)

    link = upload_to_drive(temp_path)

    os.remove(temp_path)
    confirmando(request.form, link, user_data['nome'])

    return jsonify({"status": "success"})
#-------------------------------------------------
@app.route('/salvar_membroNovo', methods=['POST'])
@token_required
def salvar_membroNovo():
    user_data = g.user_data
    file = request.files['foto']
    
    if file.filename == '':
        return "Nenhum arquivo selecionado", 400

    temp_path = os.path.join("temp", file.filename)
    os.makedirs("temp", exist_ok=True)
    file.save(temp_path)

    link = upload_to_drive(temp_path)

    os.remove(temp_path)
    confirmandoNovo(request.form, link, user_data['nome'])

    return jsonify({"status": "success"})
#-------------------------------------------------
@app.route('/consultar_cep', methods=['POST'])
@token_required
def consultar_cep():
    dados = consulta_cep(request.form.get('cep'))
    return jsonify(dados) 


@app.route('/buscar_por_membro', methods=['POST'])
@token_required
def buscar_por_membro():
    nome = request.form.get("nome")
    dados = autopreencher(nome)
    dados = dados.where(pd.notnull(dados), None)
    return jsonify(dados.to_dict()) 



def verificar_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


@socketio.on('connect')
def handle_connect():
    token = request.args.get('token')
    
    if not token or not verificar_token(token):
        disconnect()

@socketio.on('get_sugestoes')
def handle_get_sugestoes(content):
    sugestoes_response = sugestoes(content=content)
    emit('sugestoes', sugestoes_response)

if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=8025)
    