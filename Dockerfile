FROM python:3.8-alpine
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
COPY . /pipeline
WORKDIR /pipeline
RUN python setup.py develop
