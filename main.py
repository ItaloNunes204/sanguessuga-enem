import folium
curso = ''
cota = ''
notaLinguagem = ''
notaHumanas = ''
notaRedacao = ''
notaMatematica = ''
notaExatas = ''

m = folium.Map(location=[-19.92083, -43.93778])
folium.Marker(
    [-19.869089, -43.966383],popup="<i>UFMG</i>"
).add_to(m)
m.show_in_browser()
