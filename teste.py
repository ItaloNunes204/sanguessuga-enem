import requests
from bs4 import BeautifulSoup
import unidecode

def raspagem(link):
    materia = []
    peso = []
    ano = []
    modalidade = []
    nota = []

    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    resposta = requests.get('{}'.format(link),headers=headers)

    if resposta.status_code != 200:
        print("erro na busca")
        exit()

    sopao_macarronico = resposta.text
    sopa_bonita = BeautifulSoup(sopao_macarronico, 'html.parser')

    tabela = sopa_bonita.find_all("table", class_="table table-hover")

    # -----------------------------codigo duplicado-------------------------------------------
    if len(tabela)==5:
        tabela.remove(tabela[4])
        tabela.remove(tabela[3])
        tabela.remove(tabela[2])
    else:
        if len(tabela)==3:
            tabela.remove(tabela[2])
    # -----------------------------codigo duplicado-------------------------------------------

    # -----------------------------raspando materias e pesos-------------------------------------------
    tabelas = tabela
    saida = tabelas[0].find_all('td')
    # --------------------Linguagens, Códigos e suas Tecnologias
    materia.append(saida[0].text)
    peso.append(saida[1].text)
    # --------------------Matemática e suas Tecnologias
    materia.append(saida[2].text)
    peso.append(saida[3].text)
    # --------------------Ciências Humanas e suas Tecnologias
    materia.append(saida[4].text)
    peso.append(saida[5].text)
    # --------------------Ciências da Natureza e suas Tecnologias
    materia.append(saida[6].text)
    peso.append(saida[7].text)
    # --------------------Prova de Redação
    materia.append(saida[8].text)
    peso.append(saida[9].text)
    # -----------------------------raspando materias e pesos-------------------------------------------

    # -----------------------------raspando notas e modalidades-------------------------------------------
    modalidadesNotas = tabela[1]
    modalidadesNotasColunas = modalidadesNotas.find_all("tr")
    modalidadesNotasColunas.remove(modalidadesNotasColunas[0])
    for modalidadesNotasColuna in modalidadesNotasColunas:
        saidas = modalidadesNotasColuna.find_all('td')
        modalidade.append(saidas[0].text)
        nota.append(saidas[1].text)
        ano.append(modalidadesNotasColuna['class'][1])

    # -----------------------------raspando notas e modalidades-------------------------------------------
    return materia,peso,ano,modalidade,nota

def formataCurso(curso):
    curso = curso.lower()
    curso = unidecode.unidecode(curso)
    curso=curso.replace(' ','-')
    url="https://sisusimulator.com.br/curso/"+str(curso)
    return url