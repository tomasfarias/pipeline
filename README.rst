A simple data pipeline
======================

This pipeline consists of the following services:
    * A Kafka Producer which simulates real time event generation by reading events from a json file and emitting them with delay.
    * A Kafka Consumer which consumes the events and inserts them into a database.
    * A PostgreSQL database to store the data.
    * A Reporter Python app which simply runs several reports that leverage pandas. The reports can also be scheduled with cron instead of immediately run.

Running
-------

Each pipeline service runs in a docker container. After cloning the repo, to start up the pipeline do:

::

    sudo docker-compose up -d

Known issues
------------

Due to time constrains, there are a few things that do not work exactly right. The most important one is that when starting up the pipeline the consumer may fail as it tries to start when the PostgreSQL container hasn't finished bootstrapping. Wait until all other services are up and restart:

::

    sudo docker-compose restart consumer


Other services may also require a restart for similar reasons, although they're not as consistent as the consumer.


Tests
-----

Almost all services are individually unit tested with tox. To run the tests, :code:`cd` into the service directory and run :code:`tox`:

::

    cd src/consumer
    tox

All tests are written in the pytest framework.

It's running, what now?
-----------------------

Log into the database and take a look around! There's 3 tables for you to poke: :code:`orders`, :code:`events` and :code:`customers`.

::

    sudo docker exec -ti $(sudo docker ps | grep db | awk '{print $1}') bash
    psql postgres -U admin


Check out the reports produced by the reporter! There's 3 reports currently running:

    * :code:`Age`: Returns the age of all fulfilled orders in the time frame.
    * :code:`Status`: Returns the status of all orders in the time frame.
    * :code:`Estimate`: Returns amount of cancelled orders by order age in minutes.

::

    sudo docker exec -ti $(sudo docker ps | grep reporter | awk '{print $1}') bash
    cd outputs/


The reports still need fine tuning. I encourage you to play around with the :code:`end` times and :code:`offset` windows.
Also, while the jobs do get scheduled in crontab, they will probably return an empty csv since there's no recent data in the database as the events are generated from a static file.

Extending the project
---------------------

There's still a lot of stuff to do:
    * Add tests for the reporter service (coming soon).
    * Make the producer emit random events instead of only reading them from a file to have more control over the timestamp of those events.
    * Add new reports, tune the parameters.
