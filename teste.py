import requests
from bs4 import BeautifulSoup
import unidecode
import banco as bd
import pegaCoordenadas as PC
import classePin as cp


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
    cidade='https://latitudelongitude.org/br/{}/'.format(str(cidade))
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

def calculadora(notaLinguagem,notaHumanas,notaRedacao,notaMatematica,notaExatas,idUniversidade,curso):
    lista = bd.buscaPesos(idUniversidade,curso)
    pesosLinguagem,pesoHumanas,pesoRedacao,pesoMatematica,pesoExatas = trataPesos(lista)
    notaFinal = (notaLinguagem*pesosLinguagem) + (notaHumanas*pesoHumanas) + (notaRedacao*pesoRedacao) + (notaMatematica*pesoMatematica) + (notaExatas*pesoExatas)
    notaFinal = notaFinal / (pesosLinguagem + pesoHumanas + pesoRedacao + pesoMatematica + pesoExatas)
    return notaFinal

def trataPesos(pesos):
    for peso in pesos:
        if peso[4] == "Linguagens, Códigos e suas Tecnologias":
            pesoLinguagem = float(peso[5])
        elif peso[4] == "Matemática e suas Tecnologias" :
            pesoMatematica = float(peso[5])
        elif peso[4] == "Ciências Humanas e suas Tecnologias" :
            pesoHumanas = float(peso[5])
        elif peso[4] == "Ciências da Natureza e suas Tecnologias" :
            pesoExatas = float(peso[5])
        elif peso[4] == "Prova de Redação" :
            pesoRedacao = float(peso[5])
    return pesoLinguagem,pesoHumanas,pesoRedacao,pesoMatematica,pesoExatas

def adicionaCoordenadas():
    cidades=bd.buscaUniversidade()
    for cidade in cidades:
        cidade=formataCidade(cidade[1])
        coordenada=PC.pegaCoordenadas(cidade)
        print(bd.adicionaCoordenada(coordenada,cidade[0],cidade[1],cidade[2]))
    return

def comparaNotas(notaLinguagem,notaHumanas,notaRedacao,notaMatematica,notaExatas,curso,ano,Mcota):
    local=[]
    texto=[]
    corTexto=[]
    notas=bd.buscaNotasCurso(curso,ano,Mcota)
    for nota in notas:
        notaCorte = nota[7]
        idUniversidade = nota[1]
        notaUsuario = calculadora(notaLinguagem,notaHumanas,notaRedacao,notaMatematica,notaExatas,idUniversidade,curso)
        nome=nota[2]
        if notaUsuario >= notaCorte:
            #aprovado
            cor = "green"
            situacao = 'aprovado'
        else:
            #reprovado
            cor = "red"
            situacao = 'reprovado'
        if len(local) == 0:
            local.append(bd.buscaCoordenadasUniversidade(idUniversidade))
            texto.append('''<p style = "color : {}">{} : {}</p>
            <p style = "color : {}">sua nota:{}</p>
            <p style = "color : {}">nota de corte:{}</p>'''.format(cor,nome,situacao,cor,notaUsuario,cor,notaCorte))
            corTexto.append(cor)
        else:
            i=0
            while i<len(local):
                if local[i] == bd.buscaCoordenadasUniversidade(idUniversidade):
                    texto[i]=texto[i] + '''<p style = "color : {}">{} : {}</p>
                    <p style = "color : {}">sua nota:{}</p>
                    <p style = "color : {}">nota de corte:{}</p>'''.format(cor,nome,situacao,cor,notaUsuario,cor,notaCorte)
                    if corTexto[i]==cor:
                        pass
                    else:
                        corTexto[i]='purple'
                else:
                    local.append(bd.buscaCoordenadasUniversidade(idUniversidade))
                    texto.append('''<p style = "color : {}">{} : {}</p>
                    <p style = "color : {}">sua nota:{}</p>
                    <p style = "color : {}">nota de corte:{}</p>'''.format(cor,nome,situacao,cor,notaUsuario,cor,notaCorte))
                    corTexto.append(cor)
                i=i+1
    return local,texto,corTexto