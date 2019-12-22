from setuptools import setup
from setuptools import find_packages

setup(
    name='Pipeline',
    version='0.0.1',
    author='Tomas Farias',
    author_email='tomasfariassantana@gmail.com',
    description='A Python data pipeline',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'kafka-python==1.4.7',
        'python-dateutil==2.8.1',
        'pyyaml==5.2',
        'SQLAlchemy==1.3.12',
        'psycopg2==2.8.4',
    ],
    extras_require={
        'tests': [
            'pytest==5.3.2',
            'flake8==3.7.9',
            'mypy==0.761',
        ]
    },
    python_requires=">=3.7",
    entry_points={
        'console_scripts': [
            'producer = pipeline.producer:main',
            'consumer = pipeline.consumer:main',
            'init-db = pipeline.init_db:main',
        ],
    }
)
