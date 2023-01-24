import time
import requests
from bs4 import BeautifulSoup
import teste as TS
import banco as bd

def raspagem(entrada):
    curso=str(entrada)
    url=TS.formataCurso(curso)
    url_busca='https://sisusimulator.com.br'

    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    resposta = requests.get('{}'.format(url), headers=headers)

    if resposta.status_code!=200:
        print("erro na busca")
        return False

    sopao_macarronico = resposta.text
    sopa_bonita = BeautifulSoup(sopao_macarronico, 'html.parser')

    links=[]
    nomes=[]
    campus=[]
    cidade=[]

    div_tabelas = sopa_bonita.find_all('div',class_="col-sm-6 col-xs-12 result")

    for tabela in div_tabelas:
        ps=tabela.find_all('p')
        nomes.append(ps[0].text)
        campus.append(tabela.find('h3').text)
        links.append(tabela.find('a').get('href'))
        cidade.append(ps[1].text)

    i=0
    contadorMateria=0
    contadorNotas=0
    print("iniciando raspagem")
    contadorUniversidade=1
    for link in links:
        busca=url_busca+str(link)
        try:
            materias,pesos,anos,modalidades,notas=TS.raspagem(busca)
            print("universidade: " + str(nomes[i]))
            print("campus: " + str(campus[i]))
            print("cidade/estado: " + str(cidade[i]))
            print(bd.universidade(nomes[i],cidade[i],campus[i]))
            nomeUniversidade=nomes[i]
            i = i + 1
            time.sleep(1)
            print("------------pesos----------")
            while (contadorMateria < len(materias)):
                print(str(materias[contadorMateria]) + "--------" + str(pesos[contadorMateria]))
                bd.peso(nomeUniversidade,curso,materias[contadorMateria],pesos[contadorMateria])
                contadorMateria = contadorMateria + 1
            contadorMateria = 0

            print("------------fim dos pesos----------")
            time.sleep(1)
            print("------------notas----------")
            while (contadorNotas < len(modalidades)):
                print("no ano de:" + str(anos[contadorNotas]))
                print("a nota de corte na modalidade:" + str(modalidades[contadorNotas]) + "------" + str(notas[contadorNotas]))
                Mcota = TS.formataModalidade(modalidades[contadorNotas])
                bd.notas(nomeUniversidade,curso,anos[contadorNotas],modalidades[contadorNotas],float(notas[contadorNotas]),Mcota)
                contadorNotas = contadorNotas + 1
            contadorNotas = 0
            print("------------fim da notas----------")
            time.sleep(2)
            print("numero de univercidades raspadas: " + str(contadorUniversidade))
            print("numero de univercidades disponiveis: " + str(len(nomes)))
            contadorUniversidade = contadorUniversidade + 1
            print("-------------------------------------------")

        except:
            print("erro")
            print(busca)
            print("-------------------------------------------")
            print("numero de universidades raspadas: " + str(contadorUniversidade))
            print("numero de universidades disponiveis: " + str(len(nomes)))
            contadorUniversidade = contadorUniversidade + 1
            print("-------------------------------------------")
    return True
