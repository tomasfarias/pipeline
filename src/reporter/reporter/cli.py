import argparse
import sys
import datetime as dt
import os

from crontab import CronTab
from sqlalchemy import create_engine

from reporter.reports import *
from utilities import setup_logging


def main():
    args = parse_args()
    setup_logging(args.logging_config, args.debug)

    if 'schedule' not in args:
        run_reporter(args)
    else:
        schedule_reporter(args)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Run and schedule reports.'
    )
    parser.add_argument(
        '-l',
        '--logging-config',
        help='Logging configuration file',
        default='config/logging.yml'
    )
    parser.add_argument(
        '-d',
        '--debug',
        help='Toggle DEBUG logging',
        action='store_true',
    )

    sub_parsers = parser.add_subparsers(help='Report actions')

    run_parser = sub_parsers.add_parser(
        'run', help='Run a report looking back from end by offset minutes'
    )
    schedule_parser = sub_parsers.add_parser(
        'schedule', help='Schedule a report to be run at a given cron schedule'
    )

    run_parser.add_argument('name', help='Report name')
    today = dt.datetime.utcnow().isoformat()
    run_parser.add_argument(
        '-e', '--end', help='Report end time, in ISO format', type=valid_date, default=today
    )
    run_parser.add_argument(
        '-o', '--offset', help='Report offset time, in minutes', default=15, type=int
    )

    schedule_parser.add_argument('name', help='Report name')
    schedule_parser.add_argument('-s', '--schedule', help='Cron schedule', required=True)
    schedule_parser.add_argument(
        '-o', '--offset', help='Report offset time, in minutes', default=15, type=int
    )

    return parser.parse_args()


def valid_date(s):
    try:
        return dt.datetime.fromisoformat(s)
    except (ValueError, TypeError):
        raise argparse.ArgumentTypeError(f'Invalid date {s}. Try again in ISO format')


def run_reporter(args: argparse.Namespace):
    report_cls = getattr(sys.modules[__name__], args.name.title())
    engine = create_engine(
        f'postgresql://{os.environ["POSTGRES_USER"]}:{os.environ["POSTGRES_PASSWORD"]}'
        f'@db:5432/{os.environ["POSTGRES_DB"]}'
    )

    report = report_cls(
        db_engine=engine,
        end=args.end,
        offset=dt.timedelta(minutes=args.offset),
    )

    report.run()


def schedule_reporter(args: argparse.Namespace):
    cron = CronTab(user='root')
    job = cron.new(command=f'reporter run {args.name} -o {args.offset}')
    job.setall(args.schedule)
    cron.write()
