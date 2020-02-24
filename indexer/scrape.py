from celery import Celery
from elasticsearch import Elasticsearch
import json
from lxml import html
import redis
import requests
import sys
from urllib.parse import urlparse, urlunparse

SITE = 'https://adamogrady.id.au/'
r = redis.Redis(host='redis', port=6379, db=0)
app = Celery('tasks', broker='amqp://guest:guest@rabbitmq:5672')
es = Elasticsearch(hosts=[{"host":'elasticsearch'}])

@app.task
def scrape(link):
    if r.exists(link):
        return str(link)
    page = requests.get(link)
    tree = html.fromstring(page.content)
    
    links = tree.xpath('//a/@href')
    links = map(clean_url, links)
    text = tree.xpath('//body//text()')
    title = tree.xpath('//head//title//text()')
    doc = {
        'link': link,
        'title': title[0],
        'text': ','.join(text),
        'html': page.text
    }
    res = es.index(index="test-search", doc_type='page', body=doc)
    r.set(link, 1)

    for single_link in links:
        if SITE in single_link and r.exists(single_link) == 0:
            scrape.delay(single_link)
    return str(link)

def clean_url(link):
    split_url = urlparse(link)
    if split_url.netloc == '':
        split_url._replace(netloc=SITE)
    split_url._replace(fragment='')
    return urlunparse(split_url)
        
scrape.delay(SITE)