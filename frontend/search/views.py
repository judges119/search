from django.shortcuts import render
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=[{"host":'elasticsearch'}])

# Create your views here.
def index(request):
    return render(request, 'index.html')

def search(request):
    query = request.GET['query']
    page = int(request.GET.get('page', 1))
    res = es.search(index="test-search", body={
        "query": {
            "match": { "text": query }
        },
        "from": (page - 1) * 10,
        "size": 10
    })
    res['query'] = query
    res['page'] = page
    res['final'] = res['hits']['total'].get('value', 0) / 10 < page + 1
    return render(request, 'search.html', res)