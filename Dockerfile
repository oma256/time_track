FROM python:3.8-alpine

LABEL Description="Worktime Admin"
MAINTAINER Omurbek Dulatov <oma.dulatov@gmail.com>

ARG BACKEND_WEB_PORT

WORKDIR /opt/app
COPY . .

RUN apk update && \
    apk add --no-cache \
    gcc postgresql-dev musl-dev \
    postgresql-client \
    py3-pillow libxslt-dev \
    postgresql-libs libffi-dev \
    zlib-dev jpeg-dev gettext curl \
    gdal-dev geos-dev

RUN pip install -r requirements/prod.txt

RUN chmod +x /opt/app/entrypoint.sh

EXPOSE $BACKEND_WEB_PORT

ENTRYPOINT ["/opt/app/entrypoint.sh"]
