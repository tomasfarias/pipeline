from unittest import mock

from pipeline import producer


@mock.patch('sys.argv', ['', '-d', '--input', 'sample.json'])
def test_parse_ars():
    args = producer.parse_args()

    assert args.input == 'sample.json'
    assert args.debug is True


def test_get_wait_time():
    messages = [
        {'id': 1, 'timestamp': '2019-12-21 09:51:10 -0300'},
        {'id': 2, 'timestamp': '2019-12-21 09:52:10 -0300'},
    ]
    wait = producer.get_wait_time(messages, 1)

    assert wait == 60


def test_get_wait_time_no_previous_ts():
    messages = [
        {'id': 1, 'timestamp': '2019-12-21 09:51:10 -0300'},
    ]
    wait = producer.get_wait_time(messages, 0)

    assert wait == 5
