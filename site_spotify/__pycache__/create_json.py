import pycountry
from geopy.geocoders import Nominatim
import json

# to_json = {}
geolocator = Nominatim(user_agent="location")
country_geo = geolocator.geocode('Taiwan, Province of China')
print(country_geo)
# i = 0
# for country in list(pycountry.countries):
#     print(i)
#     try:
#         country_geo = geolocator.geocode(country.name)
#         location = [country_geo.latitude, country_geo.longitude]
#         to_json[country.alpha_2] = location
#         i += 1
#     except:
#         print('Fuck')
#         i += 1
#         continue
# with open('country.json', 'w') as file:
#     json.dump(to_json, file, indent=4, ensure_ascii=False)


# locations = geolocator.geocode('Canada')
# print(locations.latitude, locations.longitude)

# print(pycountry.countries.get(alpha_2 = 'TW'))