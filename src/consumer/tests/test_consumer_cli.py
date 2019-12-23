from unittest import mock

from consumer import cli

TEST_ARGS = [
    '',
    '-d',
    '-t',
    'test-topic',
    '-b',
    'test-server',
]


@mock.patch('sys.argv', TEST_ARGS)
def test_parse_ars_no_defaults():
    args = cli.parse_args()

    assert args.debug is True
    assert args.bootstrap_server == 'test-server'
    assert args.topic == 'test-topic'


@mock.patch(
    'os.environ',
    {'POSTGRES_DB': 'database', 'POSTGRES_USER': 'test', 'POSTGRES_PASSWORD': 'test'}
)
@mock.patch('sys.argv', TEST_ARGS)
@mock.patch('consumer.consumer.super')
@mock.patch('consumer.consumer.PostgreSQLConsumer.run')
def test_run_consumer(mock_run, mock_super):
    args = cli.parse_args()
    cli.run_consumer(args)

    mock_super.assert_called_once()  # should always pass
    mock_run.assert_called_once()


@mock.patch('sys.argv', [''])
def test_parse_ars_defaults():
    args = cli.parse_args()

    assert args.debug is False
    assert args.bootstrap_server == 'kafka:9092'
    assert args.topic == 'events-json-topic'
