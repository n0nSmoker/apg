#!/bin/bash
run () {
    flask init
    flask db upgrade
    gunicorn -w 4 -b 0.0.0.0:5000 run:app
}

run_dev () {
    flask init
    flask db upgrade
    FLASK_DEBUG=1 flask run --host=0.0.0.0
}

run_tests () {
    pytest --pylama --cov=app --cov-report term-missing $TEST_FILE
}


# Execute the specified command sequence
for arg
do
    $arg;
done
