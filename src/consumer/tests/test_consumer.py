import datetime as dt
from collections import namedtuple
from unittest import mock

import pytest

from consumer import consumer


@pytest.fixture
def engine():
    from sqlalchemy import create_engine

    engine = create_engine('sqlite:///:memory:')
    consumer.models.Base.metadata.create_all(engine)

    return engine


@pytest.fixture
def customer():
    return consumer.models.Customer(
        customer_id='test-123',
        registered_ts=dt.datetime(2019, 12, 21, 12, 0, 0),
        name='John',
        birthdate=dt.date(1990, 1, 1),
    )


@pytest.fixture
def test_session(engine):
    from sqlalchemy.orm import sessionmaker  # type: ignore

    session_maker = sessionmaker(bind=engine)
    return session_maker()


@pytest.fixture
def events():
    Event = namedtuple('Event', ('value', 'timestamp'))
    event0 = Event(
        value={
            'type': 'customer_registered',
            'timestamp': dt.datetime(2019, 12, 21, 12, 0, 0),
            'id': 'test-123',
            'aggregate_id': 'customer-test-123',
            'data': {"name": "John", "birthdate": "1990-01-01"},
        },
        timestamp=dt.datetime.timestamp(dt.datetime(2019, 12, 21, 12, 0, 0))
    )

    event1 = Event(
        value={
            'type': 'product_ordered',
            'timestamp': dt.datetime(2019, 12, 21, 12, 1, 0),
            'id': 'test-123',
            'aggregate_id': 'agg-test-123',
            'data': {"customer_id": "customer-test-123", "name": "Product 1"},
        },
        timestamp=dt.datetime.timestamp(dt.datetime(2019, 12, 21, 12, 1, 0))
    )

    event2 = Event(
        value={
            'type': 'order_accepted',
            'timestamp': dt.datetime(2019, 12, 21, 12, 2, 0),
            'id': 'test-123',
            'aggregate_id': 'agg-test-123',
            'data': {},
        },
        timestamp=dt.datetime.timestamp(dt.datetime(2019, 12, 21, 12, 2, 0))
    )

    events = [event0, event1, event2]
    return {
        'some-topic': events
    }


@mock.patch('consumer.consumer.super')
def test_session_scope(mock_super, engine, customer, test_session):
    from consumer import consumer
    psql_consumer = consumer.PostgreSQLConsumer(engine=engine)

    with psql_consumer.session_scope() as session:
        assert session.bind == engine
        session.add(customer)

    result = test_session.query(consumer.models.Customer).count()
    assert result == 1


@mock.patch('consumer.consumer.PostgreSQLConsumer.commit')
@mock.patch('consumer.consumer.PostgreSQLConsumer.poll')
@mock.patch('consumer.consumer.super')
def test_run_once(
    mock_super, mock_poll, mock_commit, engine, test_session, events
):
    from consumer import consumer

    psql_consumer = consumer.PostgreSQLConsumer(engine=engine)
    mock_poll.return_value = events

    psql_consumer.run_once()

    assert test_session.query(consumer.models.Customer).count() == 1
    assert test_session.query(consumer.models.Order).count() == 1

    order = test_session.query(consumer.models.Order).first()
    assert order.order_id == 'agg-test-123'
    assert order.product == 'Product 1'
    assert order.customer_id == 'customer-test-123'
    assert order.status == 'ACCEPTED'
    assert order.created_ts == dt.datetime(2019, 12, 21, 12, 1, 0)
    assert order.updated_ts == dt.datetime(2019, 12, 21, 12, 2, 0)

    customer = test_session.query(consumer.models.Customer).first()
    assert customer.customer_id == 'customer-test-123'
    assert customer.name == 'John'
    assert customer.birthdate == dt.date(1990, 1, 1)
    assert customer.registered_ts == dt.datetime(2019, 12, 21, 12, 0, 0)
