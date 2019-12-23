from unittest import mock

from dateutil import parser
import pytest

from producer import producer


@pytest.fixture
def events():
    return [
        {'id': 1, 'timestamp': '2019-12-21 09:51:10 -0300'},
        {'id': 2, 'timestamp': '2019-12-21 09:52:10 -0300'},
        {'id': 3, 'timestamp': '2019-12-21 09:53:10 -0300'},
    ]


@mock.patch('producer.producer.EventProducer.send')
@mock.patch('producer.producer.EventProducer.flush')
def test_run(mock_flush, mock_send, events):
    mock_producer = producer.EventProducer(
        max_wait=0,
        min_wait=0,
        events=[events[0]],
    )

    mock_producer.run('test-topic')

    mock_send.assert_called_once_with(
        'test-topic', {'id': 1, 'timestamp': '2019-12-21 09:51:10 -0300'}
    )
    mock_flush.assert_called_once()


def test_event(events):
    mock_producer = producer.EventProducer(
        max_wait=10,
        min_wait=2,
        events=events,
    )
    event = mock_producer.event

    assert event == {'id': 1, 'timestamp': '2019-12-21 09:51:10 -0300'}


def test_capped_get_wait_time(events):
    mock_producer = producer.EventProducer(
        max_wait=10,
        min_wait=2,
        events=events,
    )
    wait = mock_producer.get_wait_time()

    assert wait == 10

    mock_producer.events.pop(0)
    mock_producer.events.pop(0)

    wait = mock_producer.get_wait_time()

    assert wait == 2


def test_uncapped_get_wait_time(events):
    mock_producer = producer.EventProducer(
        max_wait=99999,
        min_wait=-1,
        events=events,
    )
    wait = mock_producer.get_wait_time()

    assert wait == 60

    mock_producer.events.pop(0)
    mock_producer.events.pop(0)

    wait = mock_producer.get_wait_time()

    assert wait == 0


def test_get_next_timestamp(events):
    mock_producer = producer.EventProducer(
        max_wait=10,
        min_wait=2,
        events=events,
    )
    ts = mock_producer.get_next_timestamp()
    expected = parser.parse('2019-12-21 09:52:10 -0300')

    assert ts == expected

    mock_producer.events.pop(0)
    mock_producer.events.pop(0)

    ts = mock_producer.get_next_timestamp()

    assert ts is None
