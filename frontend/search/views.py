from celery import Celery
from django.shortcuts import render
from elasticsearch import Elasticsearch
import json
import requests
from urllib import parse

es = Elasticsearch(hosts=[{"host":'elasticsearch'}])
celery = Celery('tasks', broker='amqp://guest:guest@rabbitmq:5672')

# Create your views here.
def index(request):
    return render(request, 'index.html')

def search(request):
    query = request.GET['query']
    page = request.GET.get('page', 1)
    parsed_query = parse.quote_plus(query)
    response = requests.get(f"http://query:5000/?query={parsed_query}&page={page}")
    response = response.json()
    return render(request, 'search.html', response)

def add_site(request):
    return render(request, 'add_site.html')

def added_site(request):
    url = request.GET['url']
    celery.send_task('scrape.scrape_and_spider', args=[url])
    context = {
        "url": url
    }
    return render(request, 'added_site.html', context)