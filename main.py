import folium
import teste as ts
curso = ''
cota = ''
notaLinguagem = ''
notaHumanas = ''
notaRedacao = ''
notaMatematica = ''
notaExatas = ''
cidadeUsuario=''
ano=''

lista=ts.formataCidade(cidadeUsuario)
lista=lista.split(',')

local,texto,corTexto=ts.comparaNotas(notaLinguagem,notaHumanas,notaRedacao,notaMatematica,notaExatas,curso,ano)

m = folium.Map(location=[float(lista[0]), float(lista[1])])
folium.Marker(
    location=[float(lista[0]), float(lista[1])],
    popup='''<p style = "color : red">tetste s</p>''',
    icon=folium.Icon(color="green",icon='glyphicon glyphicon-user'),
).add_to(m)
i=0
while i<len(local):
    saida=local[i].split(',')
    if corTexto == "red":
        icone='glyphicon glyphicon-remove'
    elif corTexto == "purple":
        icone='glyphicon glyphicon-search'
    else:
        icone='glyphicon glyphicon-ok'
    folium.Marker(
        location=[float(saida[0]), float(saida[1])],
        popup=texto[i],
        icon=folium.Icon(color=corTexto[i],icon=icone),
    ).add_to(m)
    i=i+1


m.show_in_browser()
