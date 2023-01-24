import requests
from bs4 import BeautifulSoup
import teste as ts

def pegaCoordenadas(cidade):
    url = ts.formataCidade(cidade)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    resposta = requests.get('{}'.format(url), headers=headers)

    if resposta.status_code!=200:
        print("erro na busca")
        exit()

    sopao_macarronico = resposta.text
    sopa_bonita = BeautifulSoup(sopao_macarronico, 'html.parser')

    dados=sopa_bonita.find_all('p')

    coordenadas=dados[0].find_all('span')

    return coordenadas[0].text
