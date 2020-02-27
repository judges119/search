from celery import Celery
from django.shortcuts import render
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=[{"host":'elasticsearch'}])
celery = Celery('tasks', broker='amqp://guest:guest@rabbitmq:5672')

# Create your views here.
def index(request):
    return render(request, 'index.html')

def search(request):
    query = request.GET['query']
    page = int(request.GET.get('page', 1))
    res = es.search(index="test-search", body={
        "query": {
            "dis_max" : {
                "queries" : [
                    {
                        "match" : {
                            "title" : {
                                "query": query,
                                "boost": 1.2
                            }
                        }
                    },
                    {
                        "match" : {
                            "text" : {
                                "query": query,
                                "boost": 1
                            }
                        }
                    }
                ],
                "tie_breaker" : 0.7
            }
        },
        "from": (page - 1) * 10,
        "size": 10
    })
    res['query'] = query
    res['page'] = page
    res['final'] = res['hits']['total'].get('value', 0) / 10 < page + 1
    return render(request, 'search.html', res)

def add_site(request):
    return render(request, 'add_site.html')

def added_site(request):
    url = request.GET['url']
    celery.send_task('scrape.scrape_and_spider', args=[url])
    context = {
        "url": url
    }
    return render(request, 'added_site.html', context)