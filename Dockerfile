FROM python:3.8-alpine

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/

RUN apk update
RUN apk add --no-cache postgresql-libs
RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

RUN pip install --no-cache-dir -r requirements.txt
RUN apk --purge del .build-deps