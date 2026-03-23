FROM python:3.13-alpine3.20
LABEL maintainer="khomutov.illia@gmail.com"

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apk add --no-cache postgresql-client jpeg-dev zlib-dev libpq-dev
RUN apk add --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN apk del .tmp-build-deps

COPY . .

RUN mkdir -p /files/media /files/static

RUN adduser \
    --disabled-password \
    --no-create-home \
    my_user

RUN chown -R my_user:my_user /files /app
RUN chmod -R 755 /files

USER my_user