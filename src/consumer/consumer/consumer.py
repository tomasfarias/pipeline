import logging
from contextlib import contextmanager
import datetime as dt
import time

import kafka  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore

from consumer import models


class PostgreSQLConsumer(kafka.KafkaConsumer):
    """Consume Kafka messages into a PostgreSQL DB"""

    def __init__(self, *topics, engine, **configs):
        super().__init__(*topics, **configs)
        self.logger = logging.getLogger(__name__)

        self.session_maker = sessionmaker(bind=engine)

    @contextmanager
    def session_scope(self):
        session = self.session_maker()
        try:
            yield session
            session.commit()
        except Exception:
            self.logger.error('rolling back session')
            session.rollback()
            raise
        finally:
            session.close()

    def run(self, wait: int = 0):
        while True:
            self.run_once()
            time.sleep(wait)  # for testing purposes

    def run_once(self):
        self.logger.info('polling for messages')
        topic_messages = self.poll()
        self.logger.debug('consumed: %s', topic_messages)

        with self.session_scope() as session:
            for _, records in topic_messages.items():
                self.logger.info('processing %s records', len(records))
                for record in records:
                    new_event = create_event(record)
                    self.logger.debug('new event: %s', new_event)

                    if new_event.event_type == 'customer_registered':
                        customer = create_customer(new_event)
                        self.logger.debug('new customer: %s', customer)
                        session.add(customer)

                    elif new_event.event_type == 'product_ordered':
                        order = create_order(new_event)
                        self.logger.debug('new order: %s', order)
                        session.add(order)

                    else:
                        status = new_event.event_type.split('_')[1].upper()
                        new_values = {
                            models.Order.status: status,
                            models.Order.updated_ts: new_event.event_ts,
                        }
                        session.query(models.Order) \
                            .filter(models.Order.order_id == new_event.aggregate_id) \
                            .update(new_values)

                    session.add(new_event)

        self.commit()


def create_event(record: kafka.consumer.fetcher.ConsumerRecord) -> models.Event:
    return models.Event(
        event_type=record.value['type'],
        event_ts=record.value['timestamp'],
        event_id=record.value['id'],
        aggregate_id=record.value['aggregate_id'],
        kafka_ts=dt.datetime.fromtimestamp(record.timestamp / 1000),
        json_data=record.value['data'],
    )


def create_customer(event: models.Event) -> models.Customer:
    return models.Customer(
        customer_id=event.aggregate_id,
        registered_ts=event.event_ts,
        name=event.json_data['name'],
        birthdate=dt.datetime.strptime(event.json_data['birthdate'], '%Y-%m-%d').date(),
    )


def create_order(event: models.Event) -> models.Order:
    return models.Order(
        order_id=event.aggregate_id,
        customer_id=event.json_data['customer_id'],
        product=event.json_data['name'],
        status='CREATED',
        created_ts=event.event_ts,
        updated_ts=event.event_ts,
    )
