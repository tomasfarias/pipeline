from unittest import mock

from producer import cli

TEST_ARGS = [
    '',
    '-d',
    '--input',
    'data/events.json',
    '-t',
    'test-topic',
    '-b',
    'test-server',
    '--max-wait',
    '100',
    '--min-wait',
    '20'
]


@mock.patch('sys.argv', TEST_ARGS)
def test_parse_ars_no_defaults():
    args = cli.parse_args()

    assert args.input == 'data/events.json'
    assert args.debug is True
    assert args.bootstrap_server == 'test-server'
    assert args.topic == 'test-topic'
    assert args.max_wait == 100
    assert args.min_wait == 20


@mock.patch('sys.argv', TEST_ARGS)
@mock.patch('producer.producer.super')
@mock.patch('producer.producer.EventProducer.run')
def test_run_producer(mock_run, mock_super, tmp_path):
    d = tmp_path / 'data'
    d.mkdir()
    p = d / 'events.json'
    p.write_text('[{"id": 123, "type": "event"}]')

    args = cli.parse_args()
    args.input = str(p)
    cli.run_producer(args)

    mock_super.assert_called_once()  # should always pass
    mock_run.assert_called_once_with(topic=args.topic)


@mock.patch('sys.argv', ['', '--input', 'sample.json'])
def test_parse_ars_defaults():
    args = cli.parse_args()

    assert args.input == 'sample.json'
    assert args.debug is False
    assert args.bootstrap_server == 'kafka:9092'
    assert args.topic == 'events-json-topic'
    assert args.max_wait == 60
    assert args.min_wait == 0
