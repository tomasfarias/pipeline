from abc import abstractmethod
import datetime as dt
import logging
from pathlib import Path

from typing import Optional


class Report:
    def __init__(
        self,
        db_engine: str,
        offset: dt.timedelta,
        end: Optional[dt.datetime] = 'now',
    ):
        self.db_engine = db_engine

        if end == 'now' or end is None:
            end = dt.datetime.now()

        self.end = end
        self.start = end - offset
        self.logger = logging.getLogger(__name__)

    def __repr__(self):
        return f'<Report {self.__name__}>'

    @abstractmethod
    def run(self):
        pass

    def save_csv(self, output):
        csv_path = Path(f'outputs/{self.__class__.__name__}/dt={self.end:%Y-%m-%dT%H:%M:%SZ}/')
        if not csv_path.exists():
            csv_path.mkdir(parents=True, exist_ok=True)

        output.to_csv(csv_path / 'report.csv', header=True, index=False, mode='w')