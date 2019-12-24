import pandas as pd

from reporter.report import Report


class Age(Report):

    def run(self):
        query = (
            "select * from orders where status = 'FULFILLED' and "
            f"updated_ts between '{self.start: %Y-%m-%d %H:%M:%S}'::timestamp and "
            f"'{self.end: %Y-%m-%d %H:%M:%S}'::timestamp"
        )
        df = pd.read_sql_query(
            query,
            con=self.db_engine,
            parse_dates=['created_ts', 'updated_ts'],
        )

        df = df.assign(  # order age in seconds
            age=(df['created_ts'] - df['updated_ts']).dt.total_seconds()
        )

        self.save_csv(df)
