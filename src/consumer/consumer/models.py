"""Our database models"""
import datetime as dt
from typing import Optional, Dict, Any

from sqlalchemy import Column, Integer, String, TIMESTAMP, JSON, Date  # type: ignore
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


class Customer(Base):
    """A single customer"""
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, nullable=False)
    customer_id = Column(String(36), nullable=False)
    registered_ts = Column(TIMESTAMP(True), nullable=False)
    name = Column(String(36), nullable=False)
    birthdate = Column(Date, nullable=False)

    def __init__(
        self,
        customer_id: str,
        registered_ts: dt.datetime,
        name: str,
        birthdate: dt.date,
    ):
        self.customer_id = customer_id
        self.registered_ts = registered_ts
        self.name = name
        self.birthdate = birthdate

    def __repr__(self) -> str:
        return f'<Customer {self.customer_id}>'


class Order(Base):
    """A single orders"""
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, nullable=False)
    order_id = Column(String(36), nullable=False)
    customer_id = Column(String(36), nullable=False)
    product = Column(String(191), nullable=False)
    status = Column(String(36), nullable=False)
    created_ts = Column(TIMESTAMP(timezone=True), nullable=False)
    updated_ts = Column(TIMESTAMP(timezone=True), nullable=False)

    def __init__(
        self,
        order_id: str,
        customer_id: str,
        product: str,
        status: str,
        created_ts: dt.datetime,
        updated_ts: dt.datetime,
    ):
        self.order_id = order_id
        self.customer_id = customer_id
        self.product = product
        self.status = status
        self.created_ts = created_ts
        self.updated_ts = updated_ts

    def __repr__(self) -> str:
        return f'<Order {self.order_id}>'
