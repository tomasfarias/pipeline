"""Start a simple Kafka producer that reads input from a file and emits messages.
It acts as a placeholder for a real life application emitting events."""
import argparse
import datetime as dt
from dateutil import parser
import json
import time
from typing import List

import kafka  # type: ignore

import pipeline.logging


def main():
    args = parse_args()

    logger = pipeline.logging.get_logger(__name__, debug=args.debug)
    logger.info('starting producer')

    producer = kafka.KafkaProducer(
        bootstrap_servers=['kafka:9092'],
        value_serializer=lambda m: json.dumps(m).encode('utf8')
    )

    with open(args.input, 'r') as f:
        json_input = json.load(f)

    for index, item in enumerate(json_input):
        wait = get_wait_time(json_input, index)

        logger.debug('sleeping for %s seconds', wait)
        time.sleep(wait)

        logger.debug('sending %s', item)
        future = producer.send('json-events-topic', item)

        try:
            record_metadata = future.get(timeout=10)
        except kafka.KafkaError as e:
            logger.error('an error occurred when sending a message', exc_info=e)
            raise

        logger.info('sent message to topic %s', record_metadata.topic)


def parse_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(description='Produce Kafka messages from a json file.')
    arg_parser.add_argument('-i', '--input', help='JSON input file', required=True)
    arg_parser.add_argument('-d', '--debug', help='Toggle DEBUG logging', action='store_true')

    return arg_parser.parse_args()


def get_wait_time(messages: List, index: int) -> int:
    if index == 0:
        return 5

    previous_ts = parser.parse(messages[index - 1]['timestamp'])
    return (
        parser.parse(messages[index]['timestamp']) - previous_ts
    ).seconds


if __name__ == '__main__':
    main()
