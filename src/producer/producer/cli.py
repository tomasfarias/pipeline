import argparse
import json

from utilities import setup_logging
from producer import producer


def main():
    args = parse_args()
    setup_logging(args.logging_config, args.debug)
    run_producer(args)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Produce Kafka messages from a json file with an artificial delay between them.'
    )
    parser.add_argument(
        '-i',
        '--input',
        help='JSON input file',
        required=True,
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
        '--max-wait',
        help='Max wait time between event emissions in seconds',
        default=60,
        type=int,
    )
    parser.add_argument(
        '--min-wait',
        help='Min wait time between event emissions in seconds',
        default=0,
        type=int,
    )
    parser.add_argument(
        '-d',
        '--debug',
        help='Toggle DEBUG logging',
        action='store_true',
    )

    return parser.parse_args()


def run_producer(args: argparse.Namespace):
    with open(args.input, 'r') as json_file:
        events = json.load(json_file)

    event_producer = producer.EventProducer(
        max_wait=args.max_wait,
        min_wait=args.min_wait,
        events=events,
        bootstrap_servers=[args.bootstrap_server],
        value_serializer=lambda m: json.dumps(m).encode('utf8')
    )

    event_producer.run(topic=args.topic)
