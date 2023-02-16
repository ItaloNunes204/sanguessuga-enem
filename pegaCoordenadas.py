from geopy.geocoders import Nominatim

def pegaCoordenadas(nome):
    try:
        locator = Nominatim(user_agent='myGeocoder')
        location = locator.geocode(nome)
        latituda = location.latitude
        longitude = location.longitude
        coordenada=str(latituda) + ',' + str(longitude)
    except:
        coordenada=None
    return coordenada
