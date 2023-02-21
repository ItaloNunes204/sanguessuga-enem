import folium
import formatacao
import banco as bd
import pegaCoordenadas as PC
curso = 'Medicina'
cota = 'L5'
notaLinguagem = '800'
notaHumanas = '720'
notaRedacao = '860'
notaMatematica = '720'
notaExatas = '680'
cidadeUsuario='ouro branco mg'
ano='2017'

usuario=PC.pegaCoordenadas(cidadeUsuario)
usuario=usuario.split(',')
m = folium.Map(location=[float(usuario[0]),float(usuario[1])])
folium.Marker(
    location=[float(usuario[0]),float(usuario[1])],
    popup='''<p style = "color : blue">usuario</p>''',
    icon=folium.Icon(color="blue",icon='glyphicon glyphicon-user'),
).add_to(m)

notas=bd.buscaNotasCurso(curso,ano,cota)
locais=[]
for nota in notas:
    idUniversidade=nota[1]
    coordenadasi=bd.buscaCoordenadasUniversidade(idUniversidade)
    notaCorte = nota[7]
    notaUsuario = formatacao.calculadora(notaLinguagem,notaHumanas,notaRedacao,notaMatematica,notaExatas,idUniversidade,curso)
    try:
        coordenadas=coordenadasi.split(',')
        if float(notaUsuario)>=float(notaCorte):
            cor='green'
            icon='glyphicon glyphicon-ok'
        else:
            cor = 'red'
            icon = 'glyphicon glyphicon-remove'
        saida=True
        for local in locais:
            if coordenadasi == local:
                folium.Marker(
                    location=[float(coordenadas[0])+0.020,float(coordenadas[1])+0.020],
                    popup='''<p style = "color :{}">
                    {}
                    <br>
                    sua nota:{} 
                    <br>
                    nota de corte {}</p>'''.format(cor,nota[2],notaUsuario,notaCorte),
                    icon=folium.Icon(color="{}".format(cor), icon="{}".format(icon)),
                ).add_to(m)
                saida=False
                break
            else:
                saida = True

        if saida==True:
            locais.append(coordenadasi)
            folium.Marker(
                location=[float(coordenadas[0]), float(coordenadas[1])],
                popup='''<p style = "color : {}">
                {} 
                <br>
                sua nota:{}
                <br> 
                nota de corte {}</p>'''.format(cor,nota[2], notaUsuario, notaCorte),
                icon=folium.Icon(color="{}".format(cor), icon="{}".format(icon)),
            ).add_to(m)
        else:
            pass
        print('pingo marcado '+nota[2])
    except:
        print('erro '+nota[2])
m.show_in_browser()
