"""Start a simple Kafka producer that reads input from a file and emits messages.
It acts as a placeholder for a real life application emitting events."""
import datetime as dt
from dateutil import parser
import logging
import time
from typing import List, Optional, Dict

import kafka  # type: ignore


class EventProducer(kafka.KafkaProducer):

    def __init__(self, max_wait: int, min_wait: int, events: List, **kwargs):
        super().__init__(**kwargs)
        self.max_wait = max_wait
        self.min_wait = min_wait
        self.logger = logging.getLogger(__name__)
        self.events = events

    @property
    def event(self):
        """The next event to be produced"""
        return self.events[0]

    def run(self, topic: str):
        """Produce all events and block until they have been sent"""
        while self.events:
            wait = self.get_wait_time()
            self.logger.debug('sleeping for %s seconds', wait)
            time.sleep(wait)

            event = self.events.pop(0)
            self.send(topic, event)\
                .add_callback(self.on_send_success, event=event)\
                .add_errback(self.on_send_failure, event=event)

        self.flush()

    def get_wait_time(self) -> int:
        """Get the time in seconds to wait before sending current event"""
        next_ts = self.get_next_timestamp()
        if next_ts is None:
            return max(0, self.min_wait)
        return min((next_ts - parser.parse(self.event['timestamp'])).seconds, self.max_wait)

    def get_next_timestamp(self) -> Optional[dt.datetime]:
        """Get the timestamp of the next event"""
        try:
            return parser.parse(self.events[1]['timestamp'])
        except IndexError:  # No more events to consume
            return None

    def on_send_success(self, record_metadata: kafka.producer.future.RecordMetadata, event: Dict):
        self.logger.info(
            'event sent: topic: %s partition: %s offset: %s',
            record_metadata.topic,
            record_metadata.partition,
            record_metadata.offset,
        )
        self.logger.debug('successful event: %s', event)

    def on_send_failure(self, error: Exception, event: Dict):
        self.logger.error('an error occurred sending event', exc_info=error)
        self.logger.debug('failed event: %s', event)
