###############################################################
# Bu program:
# - Customer tablosundan gelen json'u parse ederek listeler
# - Order tablosundan gelen json'u parse ederek listeler
# - Kullanıcıya "/customers" istegi için aramak istediği müşteri id'sorar.
# - Kullanıcıya "/orders" istegi için aramak istediği order id'sorar.
# - MapQuest API için kişisel Credential alır
# - GPS koordinatlarını MapQuest API'yı kullanarak "location" bilgisinden keşfeder.
# - MapQuest API'yı kullanarak kargo elemanına rota çizer.
# - Epoch time modülünü kullanarak ekrana zaman bilgisini formatlar.
# - Runtime'da hata vermemesi için Dictionary'de "key" olup olmadığını keşfederek kod yazar.
# - Dönen json'u konsepti "json beautifier" olan google araması ile daha okunaklı hale getirir
# - https://jsonformatter.curiousconcept.com/ sitesini referan alır
###############################################################

import requests
from urllib.parse import urlparse
import time

# region
urlCustomers = "https://northwind.netcore.io/customers.json"

rCustomers = requests.get(urlCustomers)

if not rCustomers.status_code == 200:
    raise Exception("API Bağlantı Sorunu. Status code: {}. Text: {}".format(
        rCustomers.status_code, rCustomers.text))

jsonCustomers = rCustomers.json()

urlOrders = "https://northwind.netcore.io/orders.json"

rOrders = requests.get(urlOrders)

if not rOrders.status_code == 200:
    raise Exception("API Bağlantı Sorunu. Status code: {}. Text: {}".format(
        rOrders.status_code, rOrders.text))

jsonOrders =rOrders.json()

mainMapApiUrl="http://open.mapquestapi.com/directions/v2/route"

mapApiKey="EmdoCXh6Z3KrWogOjCAJ9VA7zuP3CZL2"

def metinKontrol():
    global jsonCustomers
    #jsonCustomers2 = jsonCustomers.copy()     istege bagli
    for i in jsonCustomers["results"]:

        if len(i["contactName"]) > 15:
            i["contactName"] = i["contactName"][:15]+"..."
            #print(i["contactName"])
        if len(i["address"]) > 15:
            i["address"] = i["address"][:15]+"..."
            #print(i["address"])
        if len(i["companyName"]) > 15:
            i["companyName"] = i["companyName"][:15]+"..."
            #print(i["companyName"])
            

# 15 → Müşterileri listeleyelim
def musteriListele():
    print("Müşteri Listesi")
    print("+--------+-----------------------+-----------------------+-----------------------+-----------------------+-----------------------+")
    print("|ID      |CompanyName            |ContactName            |Address                |Country                |City                   |")
    print("+--------+-----------------------+-----------------------+-----------------------+-----------------------+-----------------------+")
    metinKontrol()
    global jsonCustomers
    
    for i in jsonCustomers["results"]:

        print(f"| {i['id']}\t |",end="")
        #print("|"+str(i['id']),end="\t |")
        print(f"{i['companyName']:<23}|",end="")
        #print(i["companyName"]+((23-len(i["companyName"]))*" "),end="|")
        print(f"{i['contactName']:<23}|",end="")
        #print(i["contactName"]+((23-len(i["contactName"]))*" "),end="|")
        print(f"{i['address']:<23}|",end="")        
        #print(i["address"]+((23-len(i["address"]))*" "),end="|")
        print(f"{i['country']:<23}|",end="")
        #print(i["country"]+((23-len(i["country"]))*" "),end="|")
        print(f"{i['city']:<23}|")
        #print(i["city"]+((21-len(i["city"]))*" "),end="|") 
        
    
    print("+--------+-----------------------+-----------------------+-----------------------+-----------------------+-----------------------+")


# 16 → Müşterileri Id'ye göre arama yapalım
def musteriAra(musteriId):
    for i in jsonCustomers["results"]:
        if i['id']==musteriId:
            #metinKontrol()   #istege bagli  setdefault burada yapilabilir
            print(f"{musteriId} ID'li müşteri bulundu. Detay Listesi")
            print("==========================")
            print(f""" 
ID                  :{i['id']}
Firma Adı           :{i["companyName"]}
Müşteri Adı         :{i["contactName"]}
İş Disiplini        :{i["contactTitle"]}
Adres               :{i["address"]}
Şehir               :{i["city"]}
Posta Kodu          :{i.setdefault("postalCode","...")}     
Ülke                :{i["country"]}
Telefon             :{i["phone"]}
Fax                 :{i.setdefault("fax","...")}            
            
            """)
            break          
            
    else:
        print(f"{musteriId} ID'li müşteri bulunamadı")


# 17 → Siparişleri listeleyelim
def siparisListele():  
    print("Sipariş Listesi")
    print("+--------+---------------+-------------------------------+-----------------------+-----------------------+---------------------+")
    print("|ID      |CustomerId     |OrderDate                      |ShipAddress            |ShipCity               |ShipCountry          |")
    print("+--------+---------------+-------------------------------+-----------------------+-----------------------+---------------------+")
    for i in jsonOrders["results"]:
        print("|"+str(i["order"]["id"]),end="\t |")
        print(i["order"]["customerId"],end="\t\t |")

        epochSaniye = i["order"]["orderDate"][6:15]
        gunumuzZamani = time.ctime(int(epochSaniye))  
        print(gunumuzZamani,end="\t |")

        if len(i["order"]["shipAddress"])>15:
            temp = i["order"]["shipAddress"][:15]+"..."
            print(temp,end="\t |")
        else:
            print(i["order"]["shipAddress"]+((23-len(i["order"]["shipAddress"]))*" "),end="|")
            
        print(i["order"]["shipCity"]+((23-len(i["order"]["shipCity"]))*" "),end="|")
        print(i["order"]["shipCountry"]+((21-len(i["order"]["shipCountry"]))*" "),end="|")
        print()
    print("+--------+---------------+-------------------------------+-----------------------+-----------------------+---------------------+")
    

# 18 → Sipariş Id'ye göre arama yapalım
def siparisAra(siparisId):
    for i in jsonOrders["results"]:

        if i["order"]["id"]==int(siparisId):
        
            epochSaniye = i["order"]["orderDate"][6:15]
            gunumuzZamani = time.ctime(int(epochSaniye))
            for a in jsonCustomers["results"]:

                if a['id']==i['order']['customerId']:
                    contact_name = a["contactName"]
                    break

            print(f"{siparisId} ID'li sipariş bulundu. Detay Listesi")
            print("==========================")
            print(f""" 
Sipariş Id          :{i['order']['id']}
Müşteri Id          :{i["order"]["customerId"]}
Firma Adı           :{i["order"]["shipName"]}
Müşteri Adı         :{contact_name}
Sipariş Tarihi      :{gunumuzZamani}
Adres               :{i["order"]["shipAddress"]}
Şehir               :{i["order"]["shipCity"]}     
Ülke                :{i["order"]["shipCountry"]}            
            """)
        
           
            nereye = i["order"]["shipCity"]     
            cevap = input(f"Kargo Rotasını {nereye.upper()} Şehri İçin Görmek İster misiniz? [e/E] :")
            if cevap.lower()=="e":
                while True:                    
                    print(f"Varış Noktası {nereye} için Rota Hesaplanacak")
                    nereden = input("Nereden Çıkacak: ")
                    print("====================================================")
                    parameters={
    "key" : mapApiKey,
    "from" : nereden,
    "to"   : nereye

} 
                    r_routes = requests.get(mainMapApiUrl,params=parameters)
                    json_routes = r_routes.json()
                    
                    print(f""" 
Kargo Rotası {nereden.upper()} den/dan {nereye.upper()} e/a/ye/ya
Toplam Süre : {json_routes["route"]['formattedTime']}
Kilometre   : {float((json_routes["route"]['distance'])*1.609344):.4}km
 ====================================================""")
                    for i in json_routes['route']['legs']:
                        for x in i["maneuvers"]:
                            print(f" {x['narrative']} ({(x['distance']*1.609344):.4}km)")
                    print("====================================================")
                         
                    break
            break
    else:
        print(f"{siparisId} ID'li sipariş bulunamadı")


def hata_kodu_1(secim):
    print(f"\n\nYanlis tuslama\t:{secim}\nLutfen menüdeki bir degeri giriniz.")

# endregion

# 19 → menu
while True:
    for i in range(5):
        print()
    secim = input("""
    Seçiminiz:
    [1]     → MÜŞTERİ LİSTELE
    [2]     → MÜŞTERİ ARA <MÜŞTERİ ID'E GÖRE>
    [3]     → SİPARİŞ LİSTELE
    [4]     → SİPARİŞ ARA <SİPARİŞ ID'E GÖRE>
    [5]     → ÇIK
    """)

    if secim.isdigit():
        secim = int(secim)
    else:
        hata_kodu_1(secim)
        continue

    if secim==1:
        musteriListele()
    elif secim==2:
        musteriId = input("Lutfen 5 haneli musteri Id'yi giriniz.\t:").upper()
        musteriAra(musteriId)
    elif secim==3:
        siparisListele()
    elif secim==4:
        siparisId = input("Lutfen 5 haneli siparis Id'yi giriniz.\t:")
        if siparisId.isdigit() : 
            siparisAra(siparisId)
        else: 
            print("Hatali tuslama")
            continue     
    elif secim==5:
        print("Iyi gunler...")
        break
    else:
        hata_kodu_1(secim)
        continue

    


 
    




     
