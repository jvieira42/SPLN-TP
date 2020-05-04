from bs4 import BeautifulSoup
import urllib3
import requests
import datetime as dt
import re
import json

http = urllib3.PoolManager()
r = http.request("GET","https://steamdb.info/sales/")

soup = BeautifulSoup(r.data, "lxml")

genRe = r'Genre:[\s]+([\w ,]+)'
devRe = r'Developer:[\s]+([\w ,]+)'
pubRe = r'Publisher:[\s]+([\w ,]+)'
rdRe = r'Release Date:[\s]+([\w ,\d]+)'

f = open('dataset.json','w');
f.write("[")
counter = 0

page = soup.tbody.find_all("tr")
for row in page:

    counter = counter+1
    print(counter)

    td_list = row.find_all("td") 
    game_page = td_list[0].a["href"]

    name = td_list[2].a.text

    discount = td_list[3].text
    price = td_list[4].text
    rating = td_list[5].text

    time_now = dt.datetime.now()
    sale_end = dt.datetime.fromtimestamp(float(td_list[6]["data-sort"])) - time_now
    sale_start = time_now - dt.datetime.fromtimestamp(float(td_list[7]["data-sort"]))
    
    # PÁGINA DO JOGO
    g = requests.get(game_page)
    
    if(g.status_code == 200):

        game = BeautifulSoup(g.content, "lxml")
        gdesc = game.find("meta",{'name': "Description"})["content"]
        gtable = game.find("div",{'class': "details_block"})

        if(gtable):
            genre = re.findall(genRe,gtable.text)
            if(genre):
                genrel = map(lambda x : x.strip(),genre[0].split(","))
            else:
                genrel = []


            developer = re.findall(devRe,gtable.text)
            if(developer):
                developerl = map(lambda x : x.strip(),developer[0].split(","))
            else:
                developerl = []


            publisher = re.findall(pubRe,gtable.text)
            if(publisher):
                publisherl = map(lambda x : x.strip(),publisher[0].split(","))
            else:
                publisherl = []

            releaseDate = re.findall(rdRe,gtable.text)
            if (releaseDate):
                releaseDate = releaseDate[0]
            else:
                releaseDate = ""


            #File write
            f.write("{\n")
            f.write(f'"name":"{name}",\n') #Nome
            f.write(f'"description":"{gdesc}",\n') #Descrição
            f.write(f'"discount":"{discount}",\n') #Desconto
            f.write(f'"price": "{price}",\n') #Preço
            f.write(f'"rating": "{rating}",\n') #Avaliação
            f.write(f'"sale_start": "{sale_start}",\n') #Inicio de promoção
            f.write(f'"sale_end": "{sale_end}",\n') #Fim de promoção
            f.write(f'"genres": {json.dumps(list(genrel))},\n') #Generos
            f.write(f'"developers": {json.dumps(list(developerl))},\n') #Developers
            f.write(f'"publishers": {json.dumps(list(publisherl))},\n') #Publisher
            f.write(f'"release_date": "{releaseDate}"\n') #Data de Lançamento
            if (counter < len(page)):
                f.write("},\n")
            else:
                f.write("}\n")

f.write("]")
f.close()
