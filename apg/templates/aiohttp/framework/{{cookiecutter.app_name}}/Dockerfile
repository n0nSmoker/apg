FROM python:3.6-alpine3.7

COPY requirements.txt /var/www/app/requirements.txt

RUN apk update && \
    apk add build-base python3-dev postgresql-dev && \
    pip3 install --upgrade pip && \
    pip3 install -r /var/www/app/requirements.txt && \
    apk del --purge build-base

WORKDIR /var/www/app
ADD . /var/www/app

HEALTHCHECK CMD curl --fail http://0.0.0.0:8080/healthz || exit 1

ENTRYPOINT ["sh", "./entrypoint.sh"]
