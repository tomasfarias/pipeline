import logging
from contextlib import contextmanager
import datetime as dt
import os

import kafka  # type: ignore
from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore

from consumer import models


class PostgreSQLConsumer(kafka.KafkaConsumer):
    """Consume Kafka messages into a PostgreSQL DB"""

    def __init__(self, *topics, **configs):
        super().__init__(*topics, **configs)
        self.logger = logging.getLogger(__name__)

        engine = create_engine(
            f'postgresql://{os.environ["POSTGRES_USER"]}:{os.environ["POSTGRES_PASSWORD"]}'
            f'@db:5432/{os.environ["POSTGRES_DB"]}'
        )
        models.Base.metadata.create_all(engine)
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

    def run(self):
        while True:
            topic_messages = self.poll()
            self.logger.debug('consumed: %s', topic_messages)

            with self.session_scope() as session:
                for _, records in topic_messages.items():
                    for record in records:
                        new_event = create_event(record)
                        self.logger.debug('new event: %s', new_event)

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
