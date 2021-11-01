import requests
from Typing import List

class API:

    def get_address_data_from_geopunt(address: str):
        data = requests.get(f"https://loc.geopunt.be/v4/Location?q={address}").json()
    #    print(data,"\n")
        info = {'address' : address,
                    'x_value' : data['LocationResult'][0]['Location']['X_Lambert72'],
                    'y_value' : data['LocationResult'][0]['Location']['Y_Lambert72'],
                    'street' : data['LocationResult'][0]['Thoroughfarename'],
                    'house_number' : data['LocationResult'][0]['Housenumber'],
                    'postcode': data['LocationResult'][0]['Zipcode'],
                    'municipality' : data['LocationResult'][0]['Municipality']}

        detail = requests.get("https://api.basisregisters.vlaanderen.be/v1/adresmatch",
                              params={"postcode": info['postcode'],
                                      "straatnaam": info['street'],
                                      "huisnummer": info['house_number']}).json()
        building = requests.get(detail['adresMatches'][0]['adresseerbareObjecten'][0]['detail']).json()
        build = requests.get(building['gebouw']['detail']).json()
        info['polygon'] = [build['geometriePolygoon']['polygon']]
    #    print(info['polygon'][0]['coordinates'][0])
    #    print(info['polygon'][1]['coordinates'][1])


        return info
