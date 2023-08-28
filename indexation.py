from elasticsearch import Elasticsearch, ElasticsearchWarning
import urllib3
import csv

# Désactiver les avertissements de sécurité non sécurisés pour les connexions Elasticsearch
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Remplacez les valeurs ci-dessous par vos informations de connexion
hosts = ["http://127.0.0.1:9200"]

# Initialisez la connexion Elasticsearch
es = Elasticsearch(hosts=hosts, verify_certs=False, timeout=30)

# Créer un index
index_name = 'articles_index'
try:
    es.indices.create(index=index_name, ignore=400)
    print(f"L'index '{index_name}' a été créé avec succès.")
except ElasticsearchWarning as ew:
    print(f"Avertissement Elasticsearch: {ew}")
except Exception as e:
    print(f"Une erreur s'est produite : {e}")

# Lire les données du fichier CSV
csv_file = 'Film_Streaming.csv'
with open(csv_file, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        document = {
            "titre": row["titre"],
            "annee": row["annee"],
            "version": row["version"],
            "qualite": row["qualité"],
            "image_url": row["image_url"]
        }
        try:
            es.index(index=index_name, body=document)
            print("Document ajouté à l'index.")
        except ElasticsearchWarning as ew:
            print(f"Avertissement Elasticsearch: {ew}")
        except Exception as e:
            print(f"Erreur lors de l'ajout du document : {e}")

print(f"Les données du fichier CSV ont été insérées dans l'index '{index_name}' avec succès.")
