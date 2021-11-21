from flask import Flask, render_template, jsonify
from sqlite3 import *
import os
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from sqlite3 import *


ua = UserAgent()
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask



def creation(bd,req):
    c = connect(bd)
    cur = c.cursor()
    res = cur.execute(req)
   
    c.close()
def ajoute(bd,job):
    req = ''' INSERT INTO job(title,lieu,date_time,description,domain,Fonction,Contrat,Entreprise,Salaire,Niveau_etude,Annonceur)
              VALUES(?,?,?,?,?,?,?,?,?,?,?) '''
    c = connect(bd)
    cur = c.cursor()
    res = cur.execute(req,job)
    c.commit()
    c.close()


def collect():
    try:
    
        os.remove("bd.sqlite")
        creation("bd.sqlite",'''create table job(title str
            ,lieu str
            ,date_time str
            ,description str
            ,domain str
            ,Fonction str
            ,Contrat str
            ,Entreprise str
            ,Salaire str
            ,Niveau_etude str
            ,Annonceur str)''')
    except:
        pass
    v = []
    list_url = []
    link_text = []
    url = "https://www.marocannonces.com/categorie/309/Emploi/Offres-emploi.html/"
    for i in range(1,50):
        list_url.append('https://www.marocannonces.com/categorie/309/Emploi/Offres-emploi/'+str(i)+'.html')

    for url in list_url:
        r = requests.get(url, headers={'User-Agent': ua.random},timeout=10)

        soup = BeautifulSoup(r.content,'html.parser')
        articles = soup.find_all('div',class_="image")
        articles2 = soup.find_all('div',class_="block_img")

    for i in articles:
        link_text.append('https://www.marocannonces.com/'+i.find('a')['href'])
    for i in articles2:
        link_text.append('https://www.marocannonces.com/'+i.find('a')['href'])

    for url in link_text:
            r = requests.get(url, headers={'User-Agent': ua.random},timeout=10)

            soup = BeautifulSoup(r.content,'html.parser')

            title = soup.find('h1').text
            lieu = soup.find('ul',class_='info-holder').find('a').text
            date_time = soup.find('ul',class_='info-holder').find_all('li')[1].text
            description = soup.find_all('div',class_='block')[1].text.replace("\n", "").replace("\r", "").replace('\t','').replace('                     ','').replace("'","\'")
            domain = soup.find('ul',class_='extraQuestionName').find('li').find('a').text
            Fonction = soup.find('ul',class_='extraQuestionName').find_all('li')[1].find('a').text
            Contrat = soup.find('ul',class_='extraQuestionName').find_all('li')[2].find('a').text
            Entreprise= soup.find('ul',class_='extraQuestionName').find_all('li')[3].find('a').text
            Salaire = soup.find('ul',class_='extraQuestionName').find_all('li')[4].find('a').text
            Niveau_etude = soup.find('ul',class_='extraQuestionName').find_all('li')[5].find('a').text
            Annonceur = soup.find('div',class_='infoannonce').find('dd').text

            job = (title,lieu,date_time,description,domain,Fonction,Contrat,Entreprise,Salaire,Niveau_etude,Annonceur)
            ajoute('bd.sqlite',job)
        




sched = BackgroundScheduler(daemon=True)
sched.add_job(collect,'interval',hours=24)
sched.start()


app = Flask(__name__)





    

def afficher(bd,req):
    allAPI = []
    c = connect(bd)
    cur = c.cursor()
    res = cur.execute(req)
    for ligne in res:
        api = {
                'title': ligne[0],
                'lieu': ligne[1],
                'date_time': ligne[2],
                'description': ligne[3],
                'domain': ligne[4],
                'Fonction': ligne[5],
                'Contrat': ligne[6],
                'Entreprise': ligne[7],
                'Salaire': ligne[8],
                'Niveau_etude': ligne[9],
                'Annonceur': ligne[10]
            }
        allAPI.append(api)
    c.close()
    return allAPI

@app.route('/api')
def GetApi():
    print("vvv")
    api = afficher('bd.sqlite','select * from job')
    return jsonify(api)



if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    
    app.run(debug=True,port=8110)

    