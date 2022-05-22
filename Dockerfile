FROM python:3.10
ENV LC_ALL en_US.UTF-8
ENV PYTHONUNBUFFERED=1
COPY ./docker/requirements.txt /opt/hulahoop/
WORKDIR /opt/hulahoop/
RUN pip3 install --no-cache-dir -r requirements.txt \
    && rm -rf ~/.cache/ && rm -rf /tmp/*
COPY ./docker/uwsgi /etc/uwsgi
COPY ./src /opt/hulahoop

#RUN python3 manage.py collectstatic --noinput

