from celery import Celery
import scrape

app = Celery('tasks', broker='amqp://guest:guest@rabbitmq:5672')

scrape.scrape_and_spider.delay("http://3g2upl4pq6kufc4m.onion/")