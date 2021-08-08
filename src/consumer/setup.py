from setuptools import setup

setup(
    name='consumer',
    version='0.0.1',
    author='Tomas Farias',
    author_email='tomasfariassantana@gmail.com',
    description='A simple Python data pipeline',
    packages=['consumer', 'utilities'],
    package_dir={'': '.'},
    install_requires=[
        'SQLAlchemy==1.3.12',
        'kafka-python==1.4.7',
        'pyyaml==5.4',
    ],
    extras_require={
        'tests': [
            'pytest==5.3.2',
            'flake8==3.7.9',
            'mypy==0.761',
            'psycopg2-binary==2.8.4',
        ]
    },
    python_requires=">=3.7",
    entry_points={
        'console_scripts': [
            'consumer = consumer.cli:main',
        ],
    }
)
