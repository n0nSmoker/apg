#!/bin/bash

run () {
    python run.py
}

run_dev () {
    gunicorn run:create_app --bind 0.0.0.0:8080 --worker-class aiohttp.GunicornUVLoopWebWorker --log-level DEBUG --reload --access-logfile - -t 3600
}

run_tests () {
    pytest --pylama --cov=app --cov-report term-missing $TEST_FILE
}

#Execute the specified command sequence
for arg
do
    $arg;
done