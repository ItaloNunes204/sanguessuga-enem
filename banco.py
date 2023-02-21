import mysql.connector
from mysql.connector import Error

try:
    con = mysql.connector.connect(host='localhost', database='enem', user='root', password='italo175933')
    cursor = con.cursor()
    conexao=True
except:
    conexao = False

def curso(nome):
    comando = """ INSERT INTO enem.curso(nome)
               VALUE (\'{}\')""".format(nome)
    try:
        cursor.execute(comando)
        con.commit()
        saida = 'curso no banco'
    except Error as e:
        saida = 'erro no banco'
    return saida

def universidade(nome,cidade,campus):
    retorno=verificadorUniversidade(nome,campus,cidade)
    if retorno != "ja cadastrado":
        comando = """ INSERT INTO enem.universidade(nome,cidade,campus)
                       VALUE (\'{}\',\'{}\',\'{}\')""".format(nome,cidade,campus)
        try:
            cursor.execute(comando)
            con.commit()
            saida = 'universidade no banco'
        except Error as e:
            saida = 'erro no banco'
    else:
        saida='ja cadastrado'
    return saida

def peso(universidade,curso,modalidade,nota,idUniversidade):
    comando = """ INSERT INTO enem.pesos(universidade,curso,modalidade,nota,idUniversidade)
                   VALUE (\'{}\' , \'{}\', \'{}\' , \'{}\',\'{}\' )""".format(universidade,curso,modalidade,str(nota),str(idUniversidade))
    try:
        cursor.execute(comando)
        con.commit()
        saida = 'nota de corte no banco'
    except Error as e:
        saida = 'erro na nota de corte'
    return saida

def notas(universidade,curso,ano,modalidade,nota,idUniversidade,Mcota):
    comando = """ INSERT INTO enem.notas(universidade,curso,ano,modalidade,nota,idUniversidade,Mcota)
                      VALUE (\'{}\',\'{}\',\'{}\',\'{}\',{},\'{}\',\'{}\')""".format(universidade,curso,ano,modalidade,float(nota),str(idUniversidade),str(Mcota))
    try:
        cursor.execute(comando)
        con.commit()
        saida = 'nota no banco'
    except Error as e:
        saida = 'erro na nota'
    return saida

def verificadorUniversidade(nome,campus,cidade):
    comando = "select*from enem.universidade where nome=\'{}\' and campus = \'{}\' and cidade = \'{}\'".format(nome,campus,cidade)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = 'curso não encontrado'
        else:
            saida = "ja cadastrado"
    except Error as e:
        saida = 'erro na busca'
    return saida

def pegaIdUniversidade(nome,campus,cidade):
    comando = "select*from enem.universidade where nome = \'{}\' and campus = \'{}\' and cidade = \'{}\'".format(nome,campus,cidade)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = 'curso não encontrado'
        else:
            saida = linhas[0][3]
    except Error as e:
        saida = 'erro na busca'
    return saida

def buscaPesos(idUniversidade,curso):
    comando = "select*from enem.pesos where idUniversidade = \'{}\' and curso = \'{}\'".format(idUniversidade,curso)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = 'curso não encontrado'
        else:
            saida = linhas
    except Error as e:
        saida = 'erro na busca'
    return saida

def adicionaCoordenada(coordenada,id):
    comando = " UPDATE enem.universidade set coordenadas = \'{}\' where id = \'{}\'".format(coordenada,id)
    try:
        cursor.execute(comando)
        con.commit()
        saida = 'coordenadas adicionadas'
    except Error as e:
        saida = 'erro ao adicionar coordenadas'
    return saida

def buscaUniversidade():
    comando = "select*from enem.universidade"
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = 'universidade não encontrado'
        else:
            saida = linhas
    except Error as e:
        saida = 'erro na busca'
    return saida

def buscaUniversidadeId(idUniversidade):
    comando = "select*from enem.universidade where id = \'{}\' ".format(idUniversidade)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = 'universidade não encontrada'
        else:
            saida = linhas[0][4]
    except Error as e:
        saida = 'erro na busca'
    return saida

def buscaNotas():
    comando = "select*from enem.notas"
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = 'nota não encontrado'
        else:
            saida = linhas
    except Error as e:
        saida = 'erro na busca'
    return saida

def buscaNotasCurso(curso,ano,Mcota):
    comando = "select*from enem.notas where curso = \'{}\' and ano=\'{}\' and Mcota=\'{}\'".format(curso,ano,Mcota)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = 'nota não encontrado'
        else:
            saida = linhas
    except Error as e:
        saida = 'erro na busca'
    return saida

def buscaNotasCorte(universidade,curso,ano,Mcota):
    comando = "select*from enem.notas where curso = \'{}\' and ano=\'{}\' and univesidade = \'{}\ and Mcota = \'{}\''".format(curso, ano,universidade,Mcota)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = 'nota não encontrado'
        else:
            saida = linhas
    except Error as e:
        saida = 'erro na busca'
    return saida

def buscaCoordenadasUniversidade(id):
    comando = "select coordenadas from enem.universidade where id={}".format(id)
    try:
        cursor.execute(comando)
        linhas = cursor.fetchall()
        if len(linhas) == 0:
            saida = 'universidade não encontrado'
        else:
            saida = linhas[0][0]
    except Error as e:
        saida = 'erro na busca'
    return saida
