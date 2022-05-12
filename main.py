import requests
import json
import pandas as pd
import csv
from unidecode import unidecode

BASE_URL = "https://kolayik.com/api/v1/"
# deneme
CAREER_ID_URL = BASE_URL + "company-structure/list-for-filter"
API_TOKEN = ""
# GITHUBA PUSHLARKEN TOKENI KALDIR
HEADERS = {"Authorization":"Bearer " + API_TOKEN}
SEARCH_METHOD = BASE_URL + "person/new-search"


# Excel olacak, gidecek exceli okuyacak (csv'de olabilir) TAMAM
# Bilgileri alacak string olarak, esdeger ID'leri bulacak (list-for-filter) TAMAM
# ID'leri dogru bir payload olusturarak save istegiyle atip kariyer olusturacak TAMAM
# Exception Handling & Belki bir raporlama (ne kadar basarili oldu, ne kadar fail oldu)

# 12.05 Commentler
# Mappingler icin test-case hazirlanacak, ozellikle calisma tipleri

def get_ID(value):
    # exception handling eklenmeli
    temp = read_from_excel()
    response = requests.request("POST", SEARCH_METHOD, headers=HEADERS, data=(value))
    if response.status_code == 200:
        json_data = json.loads(response.text)
        for item in json_data['items']:
            return json_data['items'][item]['id']
    else:
        # print(json.loads(response.text))
        return None

def read_from_excel():
    baska_array = []
    df = pd.read_excel('ege.xlsx')
    df.to_csv('testing.csv',header=True)
    with open('testing.csv','r') as csv_file:
      csv_reader = csv.reader(csv_file)
      row1 = next(csv_reader)
      for line in csv_reader:
          temp_dict = {}
          for i in row1:
              temp_dict[i] = line[row1.index(i)]
          baska_array.append(temp_dict)
    return baska_array

def find_and_match():
    temp = read_from_excel()
    listtemp = id_listing_for_career()
    general_array = []
    for n in temp:
        temp_dict = {}
        temp_array = []
        for key, value in (n.items()):
            # print(key, value)
            if key == '':
                temp_dict['order_no'] = str(int(value) + 2)
            if unidecode(key.lower()) == "baslangic tarihi":
                temp_dict['startDate'] = value
                # print({"startDate" : value})
            if unidecode(key.lower()) == "bitis tarihi":
                temp_dict['endDate'] = value
            if unidecode(key.lower()) == "calisma sekli":
                # temp_dict['employmentType'] = "fulltime"
                # fulltime, casual, contracted, freelance, parttime, mobile, intern
                if unidecode(value.lower()) == "tam zamanli":
                    temp_dict['employmentType'] = "fulltime"
                elif unidecode(value.lower()) == "gecici":
                    temp_dict['employmentType'] = "casual"
                elif unidecode(value.lower()) == "kontratli":
                    temp_dict['employmentType'] = "contracted"
                elif unidecode(value.lower()) == "serbest calisan":
                    temp_dict['employmentType'] = "freelance"
                elif unidecode(value.lower()) == "yari zamanli":
                    temp_dict['employmentType'] = "parttime"
                elif unidecode(value.lower()) == "gezici" or unidecode(value.lower()) == "mobil":
                    temp_dict['employmentType'] = "mobile"
                elif unidecode(value.lower()) == "stajyer":
                    temp_dict['employmentType'] = "intern"
            if unidecode(key.lower()) == "default":
                if unidecode(value.lower()) == "false":
                    temp_dict['default'] = (value)
                elif unidecode(value.lower()) == "true":
                    temp_dict['default'] = value
                    #temp_dict['endDate'] == None
                    del temp_dict['endDate']
            #         temp_dict['endDate'] = ""
            #     burasi bool olacak, varsayilan kariyer hatasi nedir ogrenilecek


            if unidecode(key.lower()) == "yonetici tckn":
                temp_dict['managerId'] = get_ID({"page": 1, "status": 1, "q": value})
            if unidecode(key.lower()) == "tckn ":
                temp_dict['personId'] = get_ID({"page": 1, "status": 1, "q": value})

            for t in listtemp:
                if unidecode(t['name'].lower()) == unidecode(key.lower()):
                    # print(t['id'], key)
                    for y in t['items']:
                        if unidecode(value.lower()) == unidecode(t['items'][y]['name'].lower()):
                            # print(value,t['items'][y]['id'])
                            temp_dict["companyUnitItemId[" + t['id'] + "]"] = str(t['items'][y]['id'])
                            # print({"companyUnitItemId[" + t['id'] + "]": str(t['items'][y]['id'])})
                            temp_array.append({"companyUnitItemId": str(t['items'][y]['id'])})
                    temp_dict['items'] = temp_array

        #print(temp_dict)
        general_array.append(temp_dict)

    # print(general_array)
    return (general_array)


def id_listing_for_career():
    company_structure = []
    response = requests.request("GET", CAREER_ID_URL, headers=HEADERS)
    if response.status_code == 200:
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
    else:
        print("error")
    return company_structure

def make_the_call(payload):
    # basarili ya da basarisizlarin printi
    for a in payload:
        #print(a)
        response = requests.request("POST", BASE_URL + "person-unit/save", headers={"Authorization":"Bearer " + API_TOKEN, "Content-Type":"application/json"}, data=json.dumps(a))
        if response.status_code == 200:
            print(a['order_no'] + " basarili")
            # istek basarili olduysa aksiyon ayarla
            # istek basarili oldugu icin herhangi bir aksiyon yapmamiza gerek yok

        else:
            print(a['order_no'] + " NUMARALI SATIR YUKLENEMEDİ", json.loads(response.text)['message'])


if __name__ == "__main__":
    payload = find_and_match()
    make_the_call(payload)