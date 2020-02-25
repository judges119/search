FROM python:3.8.1-alpine
RUN apk add --no-cache libxml2-dev libxslt-dev g++ python-dev
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install lxml
RUN pip install --no-cache-dir -r requirements.txt
COPY scrape.py ./
CMD [ "celery", "-A", "spider",  "worker", "--loglevel=info"]