FROM python:3.8.1-alpine
RUN apk add --no-cache libxml2-dev libxslt-dev g++ python-dev
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY scrape.py ./
CMD [ "celery", "-A", "scrape",  "worker", "--loglevel=info"]