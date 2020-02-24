FROM python:3.8.1-alpine
RUN mkdir /code
WORKDIR /code
# RUN apk add --no-cache libxml2-dev libxslt-dev g++ python-dev
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
# COPY . /code/
# CMD [ "celery", "-A", "scrape",  "worker", "--loglevel=info"]