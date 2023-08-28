import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

def scrape_film_streaming(num_pages):
    base_url = "https://filmstreamingvf.city/film-streaming/page/{}/"
    data = []

    for page in range(1, num_pages+1):
        url = base_url.format(page)
        response = requests.get(url)
        
        if response.ok:
            soup = BeautifulSoup(response.text, 'html.parser')
            titres = soup.select('div.short-item__title')
            annees = soup.select('div.film-rip')
            image_urls = soup.select('div.short-item__img  img')

            for titre, annee, image_url in zip(titres, annees, image_urls):
                annee_partition=annee.text.strip().split('\n')
                ttr = titre.text
                annee_text = annee_partition[0]if len(annee_partition) > 0 else ""
                version=annee_partition[1]if len(annee_partition) > 1 else ""
                qualité=annee_partition[2]if len(annee_partition) > 2 else ""
                img_link = "https://filmstreamingvf.city/"+image_url['data-src']
                data.append({"titre": ttr, "annee": annee_text,"version":version,"qualité":qualité, "image_url": img_link})
                
    df = pd.DataFrame(data)
    df.to_csv('Film_Streaming.csv', index=False)
    
    with open('Film_Streaming.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)
        
    print(df)
    print("Les nouvelles données ont été ajoutées aux fichiers Film_Streaming.csv et Film_Streaming.json avec succès.")

scrape_film_streaming(1100)
