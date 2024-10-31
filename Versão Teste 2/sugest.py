from Dadosgoogledrive import download_csv

download_csv()
from Dadosgoogledrive import CadastroPIB
nomes_completos = CadastroPIB["Nome Completo"].tolist()

def sugestoes(content):
    sugestoes_filtradas = [
        nome for nome in nomes_completos if nome.lower().startswith(content.lower())
    ]
    return sugestoes_filtradas
