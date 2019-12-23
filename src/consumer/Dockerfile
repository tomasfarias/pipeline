FROM python:3.8-alpine
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
COPY . /consumer
WORKDIR /consumer
RUN python setup.py install
RUN pip install psycopg2
