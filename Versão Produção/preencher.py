from sugest import CadastroPIB

def autopreencher(nome_inserido):
    if (CadastroPIB["Nome Completo"] == nome_inserido).any():
        indice = CadastroPIB[CadastroPIB["Nome Completo"] == nome_inserido].index[0]  

        return CadastroPIB.iloc[indice]