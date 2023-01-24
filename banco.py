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
    retorno=verificadorUnivercidade(nome,campus)
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

def peso(univercidade,curso,modalidade,nota):
    comando = """ INSERT INTO enem.pesos(univercidade,curso,modalidade,notaCorte)
                   VALUE ({} , {}, \'{}\' , \'{}\' )""".format(univercidade,curso,modalidade,str(nota))
    try:
        cursor.execute(comando)
        con.commit()
        saida = 'nota de corte no banco'
    except Error as e:
        saida = 'erro na nota de corte'
    return saida

def notas(univercidade,curso,ano,modalidade,nota):
    comando = """ INSERT INTO enem.notas(univercidade,curso,ano,modalidade,nota)
                      VALUE (\'{}\',\'{}\',\'{}\',\'{}\',{})""".format(univercidade,curso,ano,modalidade,nota)
    try:
        cursor.execute(comando)
        con.commit()
        saida = 'nota no banco'
    except Error as e:
        saida = 'erro na nota'
    return saida

def verificadorUnivercidade(nome,campus,cidade):
    comando = "select*from enem.univercidade where nome=\'{}\' and campus = \'{}\' and cidade = \'{}\'".format(nome,campus,cidade)
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

def buscaPesos(universidade,curso):
    comando = "select*from enem.pesos where universidade=\'{}\' and curso = \'{}\'".format(universidade,curso)
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

def adicionaCoordenada(coordenada,nome,cidade,campus):
    comando = " UPDATE enem.universidade set coordenadas = \'{}\' where nome = \"{}\" and cidade = \'{}\' and campus = \'{}\'".format(coordenada,nome,cidade,campus)
    try:
        cursor.execute(comando)
        con.commit()
        saida = True
    except Error as e:
        saida = False
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

def adicionaMcota(Mcota,id):
    comando = " UPDATE enem.universidade set Mcota = \'{}\' where id = \'{}\'".format(Mcota,id)
    try:
        cursor.execute(comando)
        con.commit()
        saida = True
    except Error as e:
        saida = False
    return saida





