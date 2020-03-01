from flask import Flask, escape, request, Response
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch(hosts=[{"host":'elasticsearch'}])

@app.route('/')
def hello():
    query = request.args.get("query", '')
    page = int(request.args.get("page", 1))
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
    return res