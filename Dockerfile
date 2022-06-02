FROM python:3.10-alpine
ENV PYTHONUNBUFFERED=1

RUN apk --update add postgresql-client

COPY requirements.txt /opt/hulahoop/
WORKDIR /opt/hulahoop/
RUN pip3 install --no-cache-dir -r requirements.txt \
    && rm -rf ~/.cache/ && rm -rf /tmp/*
COPY src /opt/hulahoop

#RUN python3 manage.py collectstatic --noinput

