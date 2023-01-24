import requests
from bs4 import BeautifulSoup
import unidecode
import banco as bd
import pegaCoordenadas as PC

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

def formataCidade(cidade):
    cidade=cidade.split('-')
    cidade = cidade[0].lower()
    cidade = unidecode.unidecode(cidade)
    cidade = cidade.replace(' ','-')
    cidade='https://latitudelongitude.org/br/{}/'.format((cidade))
    return cidade

def formataModalidade(modalidade):
    modalidade=str(modalidade)
    if modalidade == 'Ampla concorrência':
        return 'AC'
    elif modalidade == 'Candidatos com deficiência autodeclarados pretos, pardos ou indígenas que, independentemente da renda (art. 14, II, Portaria Normativa nº 18/2012), tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).':
        return 'L14'
    elif modalidade == 'Candidatos com deficiência autodeclarados pretos, pardos ou indígenas, que tenham renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo e que tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012)':
        return 'L10'
    elif modalidade == 'Candidatos com renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo que tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).' or modalidade == 'EEP - Egresso da escola pública, de baixa renda:':
        return 'L1'
    elif modalidade == 'Candidatos que, independentemente da renda (art. 14, II, Portaria Normativa nº 18/2012), tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).' or modalidade == '(as) que independentemente da renda, tenham cursado integralmente o ensino médio em escolas públicas brasileiras. (L3)' or modalidade == 'Cota Social - Egressos Escola Pública':
        return 'L5'
    elif modalidade == 'Candidatos autodeclarados pretos, pardos ou indígenas que, independentemente da renda (art. 14, II, Portaria Normativa nº 18/2012), tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).' or modalidade == '(as) autodeclarados pretos, pardos ou indígenas que, independentemente da renda, tenham cursado integralmente o ensino médio em escolas públicas brasileiras. (L4)':
        return 'L6'
    elif modalidade == 'Candidatos autodeclarados pretos, pardos ou indígenas, com renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo e que tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).':
        return 'L2'
    elif modalidade == 'Candidatos com deficiência que tenham renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo e que tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).':
        return 'L9'
    elif modalidade == 'Candidatos com deficiência que, independentemente da renda (art. 14, II, Portaria Normativa nº 18/2012), tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).':
        return 'L13'
    elif modalidade == 'Será reservada uma vaga, por curso e turno, para candidatos com necessidades educacionais especiais.' or modalidade == 'Candidatos com deficiência' or modalidade == 'Pessoa com Deficiência' or modalidade == 'PD - Pessoa com deficiência:' or modalidade == "com deficiência" or modalidade == 'com deficiência, oriundos de qualquer percurso escolar.':
        return 'PCD'
    elif modalidade == 'Cota Social - Pretos, Pardos ou Indígenas':
        return 'PCR'
    elif modalidade == 'NEEP - Negros, de baixa renda que sejam egresso de escola pública:':
        return 'NEEP'
    elif modalidade == 'IEEP - Indígena, de baixa renda, egresso de escola pública:':
        return 'IEEP'
    else:
        return 'NI'

def calculadora(notaLinguagem,notaHumanas,notaRedacao,notaMatematica,notaExatas,universidade,curso):
    pesosLinguagem,pesoHumanas,pesoRedacao,pesoMatematica,pesoExatas = trataPesos(bd.buscaPesos(universidade,curso))
    notaFinal = (notaLinguagem*pesosLinguagem) + (notaHumanas*pesoHumanas) + (notaRedacao*pesoRedacao) + (notaMatematica*pesoMatematica) + (notaExatas*pesoExatas)
    notaFinal = notaFinal / (pesosLinguagem + pesoHumanas + pesoRedacao + pesoMatematica + pesoExatas)
    return notaFinal

def trataPesos(pesos):
    for peso in pesos:
        if peso[3] == "Linguagens, Códigos e suas Tecnologias":
            pesoLinguagem = float(peso[4])
        elif peso[3] == "Matemática e suas Tecnologias" :
            pesoMatematica = float(peso[4])
        elif peso[3] == "Ciências Humanas e suas Tecnologias" :
            pesoHumanas = float(peso[4])
        elif peso[3] == "Ciências da Natureza e suas Tecnologias" :
            pesoExatas = float(peso[4])
        elif peso[3] == "Prova de Redação" :
            pesoRedacao = float(peso[4])
    return pesoLinguagem,pesoHumanas,pesoRedacao,pesoMatematica,pesoExatas

def adicionaCoordenadas():
    universidades=bd.buscaUniversidade()
    for universidade in universidades:
        cidade=formataCidade(universidade[1])
        coordenada=PC.pegaCoordenadas(cidade)
        bd.adicionaCoordenada(coordenada,universidade[0],universidade[1],universidade[2])
    return

def adicionaMcota():
    listas=bd.buscaNotas()
    for lista in listas:
        cotaFormatada = formataModalidade(lista[4])
        bd.adicionaMcota(cotaFormatada,lista[0])
    return







