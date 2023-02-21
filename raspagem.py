import requests
from bs4 import BeautifulSoup
import formatacao
import banco as bd

def abreJanela(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    resposta = requests.get('{}'.format(url), headers=headers)
    if resposta.status_code!=200:
        print("erro na busca")
        return False
    else:
        return resposta

def raspagem(entrada):
    url=formatacao.formataCurso(str(entrada))
    resposta = abreJanela(url)
    if resposta == False:
        exit()

    sopao_macarronico = resposta.text
    sopa_bonita = BeautifulSoup(sopao_macarronico, 'html.parser')

    links=[]
    nomes=[]
    campus=[]
    cidade=[]

    div_tabelas = sopa_bonita.find_all('div',class_="col-sm-6 col-xs-12 result")

    # -----------------------------pega informaçoes da universidade------------------------------------------
    for tabela in div_tabelas:
        ps=tabela.find_all('p')
        nomes.append(ps[0].text)
        campus.append(tabela.find('h3').text)
        links.append(tabela.find('a').get('href'))
        estado=formatacao.formataCidadeEstado(ps[1].text)
        cidade.append(estado)

    i=0
    contadorMateria=0
    contadorNotas=0
    contadorUniversidade=1
    for link in links:
        busca=formatacao.formataLink(link)
        try:
            # -----------------------------adiciona informaçoes da universidade------------------------------------------
            print(bd.universidade(nomes[i],cidade[i],campus[i]))
            idUniversidade=bd.pegaIdUniversidade(nomes[i],campus[i],cidade[i])
            nomeUniversidade=nomes[i]
            i = i + 1

            # -----------------------------pega dados das notas------------------------------------------
            materias, pesos, anos, modalidades, notas = raspagemNotas(busca)
            # -----------------------------adiciona informaçoes dos pesos------------------------------------------
            while (contadorMateria < len(materias)):
                bd.peso(nomeUniversidade,str(entrada),materias[contadorMateria],pesos[contadorMateria],idUniversidade)
                contadorMateria = contadorMateria + 1
            contadorMateria = 0
            # -----------------------------adiciona informaçoes das notas------------------------------------------
            while (contadorNotas < len(modalidades)):
                Mcota = formatacao.formataModalidade(modalidades[contadorNotas])
                bd.notas(nomeUniversidade,str(entrada),anos[contadorNotas],modalidades[contadorNotas],float(notas[contadorNotas]),idUniversidade,Mcota)
                contadorNotas = contadorNotas + 1
            contadorNotas = 0
        except:
            print("erro")
            print(busca)
    return True

def raspagemNotas(link):

    resposta=abreJanela(link)
    if resposta == False:
        exit()
    sopao_macarronico = resposta.text
    sopa_bonita = BeautifulSoup(sopao_macarronico, 'html.parser')

    tabela = sopa_bonita.find_all("table", class_="table table-hover")

    materia = []
    peso = []
    ano = []
    modalidade = []
    nota = []
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

    # -----------------------------raspando notas e modalidades-------------------------------------------
    modalidadesNotas = tabela[1]
    modalidadesNotasColunas = modalidadesNotas.find_all("tr")
    modalidadesNotasColunas.remove(modalidadesNotasColunas[0])
    for modalidadesNotasColuna in modalidadesNotasColunas:
        try:
            saidas = modalidadesNotasColuna.find_all('td')
            modalidade.append(saidas[0].text)
            nota.append(saidas[1].text)
            ano.append(formatacao.formataAno(modalidadesNotasColuna['class'][1]))
        except:
            print('erro no ano ' + str(modalidadesNotasColuna['class'][1]))

    # -----------------------------raspando notas e modalidades-------------------------------------------
    return materia,peso,ano,modalidade,nota
