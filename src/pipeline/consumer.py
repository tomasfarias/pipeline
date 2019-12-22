import argparse
import json
import datetime as dt

import kafka  # type: ignore

from pipeline import models
import pipeline.logging


def main():
    args = parse_args()

    logger = pipeline.logging.get_logger(__name__, debug=args.debug)
    logger.info('starting consumer')

    topic_partition = kafka.TopicPartition('json-events-topic', 0)
    consumer = kafka.KafkaConsumer(
        group_id='pipeline',
        bootstrap_servers=['kafka:9092'],
        value_deserializer=lambda m: json.loads(m),
        auto_offset_reset='earliest',
        enable_auto_commit=False,
    )
    consumer.assign([topic_partition])

    while True:
        topic_messages = consumer.poll(timeout_ms=1000)
        logger.debug('consumed %s', topic_messages)

        if not topic_messages:
            continue

        for record in topic_messages[topic_partition]:
            new_event = create_event(record)
            logger.debug('created event %s', new_event)
            print(new_event)


def parse_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(description='Consume Kafka messages.')
    arg_parser.add_argument('-d', '--debug', help='Toggle DEBUG logging', action='store_true')

    return arg_parser.parse_args()


def create_event(record: kafka.consumer.fetcher.ConsumerRecord) -> models.Event:
    return models.Event(
        event_type=record.value['type'],
        event_ts=record.value['timestamp'],
        event_id=record.value['id'],
        aggregate_id=record.value['aggregate_id'],
        kafka_ts=dt.datetime.fromtimestamp(record.timestamp / 1000),
        json_data=record.value['data'],
    )


if __name__ == '__main__':
    main()
