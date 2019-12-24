import pandas as pd

from reporter.report import Report


class Status(Report):

    def run(self):
        query = (
            'select * from orders where '
            f"updated_ts between '{self.start: %Y-%m-%d %H:%M:%S}'::timestamp and "
            f"'{self.end: %Y-%m-%d %H:%M:%S}'::timestamp"
        )
        df = pd.read_sql_query(
            query,
            con=self.db_engine,
            parse_dates=['created_ts', 'updated_ts'],
        )

        df = df.groupby('status').size().reset_index(name='counts')

        self.save_csv(df)
