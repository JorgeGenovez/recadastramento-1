import os
from flask import Flask
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
import json

app = Flask(__name__)
Ftoken = "Ftoken.json"
CLIENT_SECRET_FILE = "credentials.json"
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def upload_to_drive(file_path):

    if os.path.exists(Ftoken):
        creds = Credentials.from_authorized_user_file(Ftoken, SCOPES)
        
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(Ftoken, 'w') as token:
                token.write(creds.to_json())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(Ftoken, 'w') as token:
            token.write(creds.to_json())
    
    service = build('drive', 'v3', credentials=creds)
    with open('Foto.json') as json_file:
        FOLDER_ID = json.load(json_file)['SECRET_KEY'] 
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [FOLDER_ID]
    }
    
    media = MediaFileUpload(file_path, mimetype='image/jpeg')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    file_id = file.get('id')
    service.permissions().create(
        fileId=file_id,
        body={'type': 'anyone', 'role': 'reader'}
    ).execute()

    link_foto = f"https://drive.google.com/thumbnail?sz=w500&id={file_id}"
    return link_foto
