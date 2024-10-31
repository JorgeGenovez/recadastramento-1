from flask import Flask
import os
import json
import pandas as pd
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

app = Flask(__name__)
CadastroPIB = pd.DataFrame()

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
CLIENT_SECRET_FILE = "credentials.json"
Dtoken = "Dtoken.json"

@app.route('/download_csv', methods=['GET'])
def download_csv():
    global CadastroPIB
    if os.path.exists('arquivo.csv'):
        CadastroPIB = pd.read_csv('arquivo.csv')
    else:
        if os.path.exists(Dtoken):
            creds = Credentials.from_authorized_user_file(Dtoken, SCOPES)

            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                with open(Dtoken, 'w') as token:
                    token.write(creds.to_json())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
            with open(Dtoken, 'w') as token:
                token.write(creds.to_json())

        service = build('drive', 'v3', credentials=creds)
        with open('Dados.json') as json_file:
            file_id = json.load(json_file)['SECRET_KEY']

        request = service.files().export_media(fileId=file_id, mimeType='text/csv')
        file_content = request.execute()

        with open('arquivo.csv', 'wb') as f:
            f.write(file_content)

        CadastroPIB = pd.read_csv('arquivo.csv')

if __name__ == '__main__':
    app.run(debug=True)
