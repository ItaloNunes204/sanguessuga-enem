from geopy.geocoders import Nominatim
try:
    locator=Nominatim(user_agent='myGeocoder')
    location=locator.geocode('OURO BRANCO')
    latituda=location.latitude
    longitude=location.longitude
    print(str(latituda)+','+str(longitude))
except:
    print('erro na ')