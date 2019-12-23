import datetime as dt
from typing import Optional, Dict, Any

from sqlalchemy import Column, Integer, String, TIMESTAMP, JSON  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore

Base = declarative_base()  # type: Any


class Event(Base):
    """A single event"""
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, nullable=False)
    event_type = Column(String(50), nullable=False)
    event_ts = Column(TIMESTAMP(True), nullable=False)
    event_id = Column(String(36), nullable=False)
    aggregate_id = Column(String(36), nullable=False)
    kafka_ts = Column(TIMESTAMP(timezone=True), nullable=False)
    json_data = Column(JSON(none_as_null=False), nullable=True)

    def __init__(
        self,
        event_type: str,
        event_ts: dt.datetime,
        event_id: str,
        aggregate_id: str,
        kafka_ts: dt.datetime,
        json_data: Optional[Dict] = None
    ):
        self.event_type = event_type
        self.event_ts = event_ts
        self.event_id = event_id
        self.aggregate_id = aggregate_id
        self.kafka_ts = kafka_ts
        self.json_data = json_data

    def __repr__(self) -> str:
        return f'<Event {self.event_type}, {self.event_id}>'
