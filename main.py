import requests
import json

BASE_URL = "https://kolayik.com/api/v1/"

CAREER_ID_URL = BASE_URL + "company-structure/list-for-filter"
API_TOKEN = ""
# GITHUBA PUSHLARKEN TOKENI KALDIR
HEADERS = {"Authorization":"Bearer " + API_TOKEN}

# Excel olacak, gidecek exceli okuyacak (csv'de olabilir)
# Bilgileri alacak string olarak, esdeger ID'leri bulacak (list-for-filter)
# ID'leri dogru bir payload olusturarak save istegiyle atip kariyer olusturacak
# Exception Handling & Belki bir raporlama (ne kadar basarili oldu, ne kadar fail oldu)

def id_listing_for_career():
    company_structure = []
    response = requests.request("GET", CAREER_ID_URL, headers=HEADERS)
    for i in json.loads(response.text)['data']:
        # print(json.loads(response.text)['data'][i])
        temp_object = {
            "id": json.loads(response.text)['data'][i]['id'],
            "name": json.loads(response.text)['data'][i]['name'],
            "items": json.loads(response.text)['data'][i]['items'],
            "sequence": json.loads(response.text)['data'][i]['sequence'],
            "status": json.loads(response.text)['data'][i]['status'],
        }
        company_structure.append(temp_object)
    return company_structure

if __name__ == "__main__":
    temp = (id_listing_for_career())
    for i in temp:
        print(i['name'] + ":")
        for t in i['items']:
            print(i['items'][t]['name'])

