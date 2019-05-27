FROM python:3.6-alpine3.7

COPY requirements.txt /var/www/app/requirements.txt

RUN apk update && \
    apk add build-base postgresql-dev python3-dev libffi-dev zlib-dev jpeg-dev git && \
    pip3 install --no-cache-dir --upgrade pip
RUN pip3 install -r /var/www/app/requirements.txt --no-cache-dir && \
    apk del --purge build-base
    
WORKDIR /var/www/app
ADD . /var/www/app

ENV FLASK_APP ./run.py

ENTRYPOINT ["sh", "./entrypoint.sh"]
