from setuptools import setup

setup(
    name='reporter',
    version='0.0.1',
    author='Tomas Farias',
    author_email='tomasfariassantana@gmail.com',
    description='A simple Python data pipeline',
    packages=['reporter', 'utilities', 'reporter.reports'],
    package_dir={'': '.'},
    install_requires=[
        'pandas==0.25.1',
        'python-crontab==2.4.0',
        'pyyaml==5.4',
        'SQLAlchemy==1.3.12',
        'psycopg2-binary==2.8.4',
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
            'reporter = reporter.cli:main',
        ],
    }
)
