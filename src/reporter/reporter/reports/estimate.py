import pandas as pd

from reporter.report import Report


class Estimate(Report):

    def run(self):
        query = (
            "select * from orders where status = 'CANCELLED' and "
            f"updated_ts between '{self.start: %Y-%m-%d %H:%M:%S}'::timestamp and "
            f"'{self.end: %Y-%m-%d %H:%M:%S}'::timestamp"
        )
        df = pd.read_sql_query(
            query,
            con=self.db_engine,
            parse_dates=['created_ts', 'updated_ts'],
        )

        df = df.assign(  # order age in minutes
            age=(df['created_ts'] - df['updated_ts']).dt.total_seconds() // 60
        )

        df.groupby('age').size().reset_index(name='counts')

        self.save_csv(df)
