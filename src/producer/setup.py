from setuptools import setup

setup(
    name='producer',
    version='0.0.1',
    author='Tomas Farias',
    author_email='tomasfariassantana@gmail.com',
    description='A simple Python data pipeline',
    packages=['producer', 'utilities'],
    package_dir={'': '.'},
    install_requires=[
        'kafka-python==1.4.7',
        'python-dateutil==2.8.1',
        'pyyaml==5.2',
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
            'producer = producer.cli:main',
        ],
    }
)
