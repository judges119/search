from celery import Celery
from datetime import datetime
from elasticsearch import Elasticsearch
import json
from lxml import html
import re
import redis
import requests
import sys
from urllib.parse import urlparse, urlunparse

r = redis.Redis(host='redis', port=6379, db=0)
app = Celery('tasks', broker='amqp://guest:guest@rabbitmq:5672')
es = Elasticsearch(hosts=[{"host":'elasticsearch'}])

proxies = {
    "http": "socks5h://tor:9150",
    "https": "socks5h://tor:9150",
}

def scrape(link):
    now = datetime.now()
    parsed_link = urlparse(link)
    if not parsed_link.hostname.endswith('.onion'):
        return []
    if r.exists(link):
        return []
    r.set(link, now)
    page = requests.get(link, proxies=proxies)
    tree = html.fromstring(page.content)
    
    # Ignore RSS files
    if tree.xpath('boolean(//rss)'):
        return []
    
    links = tree.xpath('//a/@href')
    for index, found_link in enumerate(links):
        links[index] = [found_link, link]
    links = map(clean_url, links)
    text = tree.xpath('//body//text()')
    title = tree.xpath('//head//title//text()')
    doc = {
        'link': link,
        'title': title[0] if len(title) > 0 else None,
        'text': ','.join(text),
        'html': page.text,
        'scanned_timestamp': now
    }
    res = es.index(index="test-search", doc_type='page', body=doc)
    return links

def clean_url(link):
    split_found_url = urlparse(link[0])
    split_crawled_url = urlparse(link[1])
    if split_found_url.scheme == '':
        split_found_url = split_found_url._replace(scheme=str(split_crawled_url.scheme))
    if split_found_url.netloc == '':
        split_found_url = split_found_url._replace(netloc=str(split_crawled_url.netloc))
    split_found_url = split_found_url._replace(fragment='')
    return urlunparse(split_found_url)

def spider_links(links):
    for single_link in links:
        if r.exists(single_link) == 0:
            scrape_and_spider.delay(single_link)

def delete_link(link):
    r.delete(link)
    res = es.delete_by_query(index="test-search", doc_type='page', body={
        "query": {
            "match_phrase": {
                "link": link
            }
        }
    })

@app.task
def scrape_and_spider(link):
    if r.dbsize() > 4000:
        return str(link)
    links = scrape(link)
    spider_links(links)
    return str(link)