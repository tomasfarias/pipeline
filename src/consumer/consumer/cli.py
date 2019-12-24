"""The consumer CLI. Handles logging, database initialization and running the consumer"""
import argparse
import json
import os

from sqlalchemy import create_engine  # type: ignore

from utilities import setup_logging
from consumer import consumer
from consumer import models


def main():
    args = parse_args()
    setup_logging(args.logging_config, args.debug)
    run_consumer(args)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Consume messages into a PostgreSQL DB.'
    )
    parser.add_argument(
        '-t',
        '--topic',
        help='Kafka topic',
        default='events-json-topic',
    )
    parser.add_argument(
        '-b',
        '--bootstrap-server',
        help='Kafka bootstrap server',
        default='kafka:9092'
    )
    parser.add_argument(
        '-l',
        '--logging-config',
        help='Logging configuration file',
        default='config/logging.yml'
    )
    parser.add_argument(
        '-d',
        '--debug',
        help='Toggle DEBUG logging',
        action='store_true',
    )

    return parser.parse_args()


def run_consumer(args: argparse.Namespace):
    engine = create_engine(
        f'postgresql://{os.environ["POSTGRES_USER"]}:{os.environ["POSTGRES_PASSWORD"]}'
        f'@db:5432/{os.environ["POSTGRES_DB"]}'
    )
    models.Base.metadata.create_all(engine)

    postgresql_consumer = consumer.PostgreSQLConsumer(
        args.topic,
        engine=engine,
        group_id='consumer-group',
        max_poll_records=1,
        bootstrap_servers=[args.bootstrap_server],
        value_deserializer=lambda m: json.loads(m),
        auto_offset_reset='earliest',
        enable_auto_commit=False,
    )

    postgresql_consumer.run(wait=5)
