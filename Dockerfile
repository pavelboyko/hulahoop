# we don't use alpine because there are no wheels for matplotlib and numpy yet, see https://pythonspeed.com/articles/alpine-docker-python/ 
FROM python:3.10-bullseye
ENV PYTHONUNBUFFERED=1

RUN apt update && \
    apt install -y netcat

COPY requirements.txt /opt/hulahoop/
WORKDIR /opt/hulahoop/
RUN pip install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt && \
    rm -rf ~/.cache/ && rm -rf /tmp/*

COPY src /opt/hulahoop

ENTRYPOINT ["/opt/hulahoop/entrypoint.sh"]

