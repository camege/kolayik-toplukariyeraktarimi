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
# 
# 
# 


# Excel olacak, gidecek exceli okuyacak (csv'de olabilir)
# Bilgileri alacak string olarak, esdeger ID'leri bulacak (list-for-filter)
# ID'leri dogru bir payload olusturarak save istegiyle atip kariyer olusturacak
# Exception Handling & Belki bir raporlama (ne kadar basarili oldu, ne kadar fail oldu)

def read_from_excel():
    baska_array = []
    df = pd.read_excel('test_toplukariyeraktarimi.xlsx')
    df.to_csv('testing.csv',header=True)
    with open('testing.csv','r') as csv_file:
      csv_reader = csv.reader(csv_file)
      row1 = next(csv_reader)
      for line in csv_reader:
          temp_dict = {}
          for i in row1:
              temp_dict[i] = line[row1.index(i)]
          # print(temp_dict)
          baska_array.append(temp_dict)
    return baska_array

def find_and_match():
    temp = read_from_excel()
    listtemp = id_listing_for_career()
    for key,value in (temp[0].items()):
        for t in listtemp:
            if unidecode(t['name'].lower()) == unidecode(key.lower()):
                print(t['name'], key)
                for y in t['items']:
                    if unidecode(value.lower()) == unidecode(t['items'][y]['name'].lower()):
                        print(value,t['items'][y]['name'])

#   esitlik yoksa ne yapacagiz? hata verip, yapmayabiliriz, programi durdurabiliriz
#   exception handling (try/catch)
#   satir satir loglayabiliriz yaptik yapamadik diye

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
        # {
        #     'companyUnitItemId[' + hiyerarsidekiyeri + ']': unvan,
        # }
        company_structure.append(temp_object)
    return company_structure

if __name__ == "__main__":
    # temp = (read_from_excel())
    find_and_match()
    # print(unidecode('çamlıbel'))
    # temp = (id_listing_for_career())
    # for i in temp:
    #     print(i['name'] + ":")
    #     for t in i['items']:
    #         print(i['items'][t]['name'])

