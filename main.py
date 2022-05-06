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

def get_ID(value):
    response = requests.request("POST", SEARCH_METHOD, headers=HEADERS, data=(value))
    json_data = json.loads(response.text)
    for item in json_data['items']:
        return json_data['items'][item]['id']

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
    temp_dict = {}
    temp_array = []
    for key,value in (temp[0].items()):
        # print(key, value)
        if unidecode(key.lower()) == "baslangic tarihi":
            print(value[:5] + value[6:])
            temp_dict['startDate'] = value[:5] + value[6:]
            # print({"startDate" : value})
        if unidecode(key.lower()) == "bitis tarihi":
            temp_dict['endDate'] = value[:5] + value[6:]
        if unidecode(key.lower()) == "calisma sekli":
            temp_dict['employmentType'] = "fulltime"
        #     if value == "":
        #         temp_dict['employmentType'] = "fulltime"
        #     elif value == "":
        #         temp_dict['employmentType'] = "parttime"
        if unidecode(key.lower()) == "default":
            temp_dict['default'] = value
        if unidecode(key.lower()) == "yonetici tckn":
            temp_dict['managerId'] = get_ID({"page": 1, "status": 1, "q": value})
        if unidecode(key.lower()) == "tckn ":
            temp_dict['personId'] = get_ID({"page": 1, "status": 1, "q": value})

        # bitis tarihi, calisma sekli, yonetici tckn, tckn

        for t in listtemp:
            if unidecode(t['name'].lower()) == unidecode(key.lower()):
                # print(t['id'], key)
                for y in t['items']:
                    if unidecode(value.lower()) == unidecode(t['items'][y]['name'].lower()):
                        # print(value,t['items'][y]['id'])
                        temp_dict["companyUnitItemId[" + t['id'] + "]"] = str(t['items'][y]['id'])
                        # print({"companyUnitItemId[" + t['id'] + "]": str(t['items'][y]['id'])})
                        temp_array.append({"companyUnitItemId":str(t['items'][y]['id'])})
    # print(temp_array)
    temp_dict['items'] = temp_array
    # print(temp_dict)
    return(temp_dict)


#   esitlik yoksa ne yapacagiz? hata verip, yapmayabiliriz, programi durdurabiliriz
#   exception handling (try/catch)
#   satir satir loglayabiliriz yaptik yapamadik diye

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
            # {
            #     'companyUnitItemId[' + hiyerarsidekiyeri + ']': unvan,
            # }
            company_structure.append(temp_object)
    else:
        print("error")
    return company_structure

def make_the_call(payload):
    print(payload)
    response = requests.request("POST", BASE_URL + "person-unit/save", headers={"Authorization":"Bearer " + API_TOKEN, "Content-Type":"application/json"}, data=json.dumps(payload))
    if response.status_code == 200:
        print("basarili")
        # istek basarili olduysa aksiyon ayarla
    else:
        print(response.text)

if __name__ == "__main__":
    # temp = (read_from_excel())
    payload = find_and_match()
    make_the_call(payload)
    # print(unidecode('çamlıbel'))
    # temp = (id_listing_for_career())
    # for i in temp:
    #     print(i['name'] + ":")
    #     for t in i['items']:
    #         print(i['items'][t]['name'])

