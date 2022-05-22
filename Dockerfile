FROM python:3.10
ENV PYTHONUNBUFFERED=1

RUN \
  apt update && \
  apt install -yq --reinstall ca-certificates && \
  apt install -yq \
    postgresql-client

COPY requirements.txt /opt/hulahoop/
WORKDIR /opt/hulahoop/
RUN pip3 install --no-cache-dir -r requirements.txt \
    && rm -rf ~/.cache/ && rm -rf /tmp/*
COPY src /opt/hulahoop

#RUN python3 manage.py collectstatic --noinput

