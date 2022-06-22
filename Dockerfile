# we don't use alpine because there are no wheels for matplotlib and numpy yet, see https://pythonspeed.com/articles/alpine-docker-python/ 
FROM python:3.10-bullseye
ENV PYTHONUNBUFFERED=1

RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - && \
    echo "deb http://apt.postgresql.org/pub/repos/apt/ bullseye-pgdg main" | tee /etc/apt/sources.list.d/postgresql-pgdg.list > /dev/null && \
    apt update && \
    apt install -yq postgresql-client-14

COPY requirements.txt /opt/hulahoop/
WORKDIR /opt/hulahoop/
RUN pip3 install --no-cache-dir -r requirements.txt \
    && rm -rf ~/.cache/ && rm -rf /tmp/*

COPY src /opt/hulahoop

#RUN python3 manage.py collectstatic --noinput

