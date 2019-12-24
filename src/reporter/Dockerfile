FROM python:3.7.5-slim
RUN apt-get update \
 && apt-get install -y gcc python3-dev python3-pip musl-dev \
 libxml2-dev libxslt1-dev zlib1g-dev g++ cron \
 && apt-get clean
COPY . /reporter
WORKDIR /reporter
RUN python3.7 setup.py install

CMD sh entrypoint.sh
