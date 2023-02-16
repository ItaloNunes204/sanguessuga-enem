import unidecode
import banco as bd
import pegaCoordenadas

def formataAno(ano):
    ano=ano.split('_')
    return ano[0]

def formataCurso(curso):
    curso = curso.lower()
    curso = unidecode.unidecode(curso)
    curso=curso.replace(' ','-')
    url="https://sisusimulator.com.br/curso/"+str(curso)
    return url

def formataNome(nome):
    nome=nome.split('-')
    return nome[1]

def formataCidadeEstado(dado):
    saida=dado.split('(')
    return saida[0]

def formataCidade(entrada):
    entrada=entrada.split('-')
    return entrada

def formataModalidade(modalidade):
    modalidade=str(modalidade)
    if modalidade == 'Ampla concorrência' and modalidade=='Ampla Concorrência':
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
    notaFinal = (float(notaLinguagem)*pesosLinguagem) + (float(notaHumanas)*pesoHumanas) + (float(notaRedacao)*pesoRedacao) + (float(notaMatematica)*pesoMatematica) + (float(notaExatas)*pesoExatas)
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
    dados = bd.buscaUniversidade()
    contador = 0
    for dado in dados:
        cidade = formataCidade(dado[1])
        nome = formataNome(dado[0])
        saida = str(nome) + ' ' + str(cidade[0])
        coordenada = pegaCoordenadas.pegaCoordenadas(saida)
        if not coordenada:
            coordenada = pegaCoordenadas.pegaCoordenadas(nome)
            if not coordenada:
                coordenada = pegaCoordenadas.pegaCoordenadas(dado[2])
                if not coordenada:
                    coordenada = pegaCoordenadas.pegaCoordenadas(cidade[0])
                    if not coordenada:
                        print(dado[0] + " " + saida)
                        contador = contador + 1
    print(contador)