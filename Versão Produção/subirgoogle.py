import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def confirmando(dados, link, quem_cadastrou):
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    SPREADSHEET_ID = "197dGyWjtAVUVR2K8eODfIxfrEFgeErTcxMhp3OIX8N0"
    RANGE_NAME = "DadosNovo!A1:AY3000"

    creds = None
    Stoken = "Stoken.json"

    if os.path.exists(Stoken):
        creds = Credentials.from_authorized_user_file(Stoken, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open(Stoken, "w") as token:
            token.write(creds.to_json())
    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        dados = {
                "Foto": [str(link)],
                "Nome Completo": [str(dados['nome_completo'])],
                "Matrícula": [str(dados['matricula'])], 
                #"CPF": [str(dados['cpf'])], 
                "Data de Nascimento": [str(dados['data_de_nascimento'])],  
                #"Sexo": [str(dados['sexo'])],  
                "Tipo Sanguíneo": [str(dados['tipo_sanguineo'])],  
                "Estado Civil": [str(dados['estado_civil'])],  
                "Data de Casamento": [str(dados['data_de_casamento'])],  
                #"Profissão": [str(dados['profissao'])],  
                "Naturalidade": [str(dados['naturalidade'])], 
                "Nacionalidade": [str(dados['nacionalidade'])], 
                "Rua": [str(dados['rua'])], 
                "Complemento": [str(dados['complemento'])],  
                "Bairro": [str(dados['bairro'])], 
                "Município": [str(dados['cidade'])],  
                "Estado": [str(dados['estado'])],  
                "CEP": [str(dados['cep'])],  
                "Tel. Residencial": [str(dados['telefone_residencial'])],  
                "Tel. Celular": [str(dados['telefone_celular'])],  
                "E-mail": [str(dados['email'])],  
                "Nome do Pai": [str(dados['nome_do_pai'])],  
                "Pai Membro": [str(dados['pai_eh_membro'])],
                "Nome da Mãe": [str(dados['nome_mae'])], 
                "Mãe Membro": [str(dados['mae_eh_membro'])],
                "Nome do Conjuge": [str(dados['nome_conjuge'])],
                "Data de Nascimento Conjuge": [str(dados['data_de_nascimento_do_conjuge'])],
                "Conjuge Membro": [str(dados['conjuge_eh_membro'])],
                "Cargo atual": [str(dados['cargo_atual'])],
                "Data Batismo": [str(dados['data_de_batismo'])],
                "Igreja Batismo": [str(dados['igreja_de_batismo'])],
                "Bairro Igreja Batismo":[str(dados['bairro_da_igreja_de_batismo'])],
                "Data de Entrada PIB": [str(dados['data_em_que_virou_membro'])],
                "Forma de entrada": [str(dados['modo'])],
                "Nome do filho(a) 1": [str(dados['nome_do_filho1'])],
                "Data de Nascimento do filho(a) 1": [str(dados['data_de_nascimento_do_filho1'])],
                "Seu filho(a) 1 é membro da PIB Pavuna?": [str(dados['filho1_eh_membro'])],
                "Nome do filho(a) 2": [str(dados['nome_do_filho2'])],
                "Data de Nascimento do filho(a) 2": [str(dados['data_de_nascimento_do_filho2'])],
                "Seu filho(a) 2 é membro da PIB Pavuna?": [str(dados['filho2_eh_membro'])],
                "Nome do filho(a) 3": [str(dados['nome_do_filho3'])],
                "Data de Nascimento do filho(a) 3": [str(dados['data_de_nascimento_do_filho3'])],
                "Seu filho(a) 3 é membro da PIB Pavuna?": [str(dados['filho3_eh_membro'])],
                "Nome do filho(a) 4": [str(dados['nome_do_filho4'])],
                "Data de Nascimento do filho(a) 4": [str(dados['data_de_nascimento_do_filho4'])],
                "Seu filho(a) 4 é membro da PIB Pavuna?": [str(dados['filho4_eh_membro'])],
                "Nome do filho(a) 5": [str(dados['nome_do_filho5'])],
                "Data de Nascimento do filho(a) 5": [str(dados['data_de_nascimento_do_filho5'])],
                "Seu filho(a) 5 é membro da PIB Pavuna?": [str(dados['filho5_eh_membro'])],
                "Cadastrante": [str(quem_cadastrou)]
        }

        valores = [[v[0] for v in dados.values()]]

        request = sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body={"values": valores},
        )
        response = request.execute()
    except HttpError as error:
        pass
