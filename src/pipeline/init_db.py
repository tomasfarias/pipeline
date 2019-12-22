import os

from sqlalchemy import create_engine  # type: ignore

from pipeline.models import Base


def main():
    db_name = os.environ.get('POSTGRES_DB', 'postgres')
    db_username = os.environ.get('POSTGRES_USER', 'postgres')
    db_password = os.environ.get('POSTGRES_PASSWORD')
    db_uri = f'postgresql://{db_username}:{db_password}@db:5432/{db_name}'
    engine = create_engine(db_uri)

    Base.metadata.create_all(engine)


if __name__ == '__main__':
    main()
