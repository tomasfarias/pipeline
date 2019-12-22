FROM python:3.8-alpine
COPY . /pipeline
WORKDIR /pipeline
RUN python setup.py develop
