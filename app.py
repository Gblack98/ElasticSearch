from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
import urllib3

app = Flask(__name__, template_folder="templates")

# Configuration Elasticsearch
hosts = ["http://127.0.0.1:9200"]
es = Elasticsearch(hosts=hosts, verify_certs=False, timeout=30)

# Route de recherche
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')

    # Recherche Elasticsearch avec tolérance aux fautes d'orthographe
    search_body = {
  "query":{
    "bool": {
      "should": [
        {
          "match": {
      "titre": query
        }
      }]
    }  
  }
}


    # Exécute la recherche
    try:
        response = es.search(index='articles_index', body=search_body)
        results = response['hits']['hits']
    except Exception as e:
        print(f"Erreur lors de la recherche : {e}")
        results = []

    return render_template('search_results.html', query=query, results=results)


if __name__ == '__main__':
    app.run(debug=True, port=8080)

