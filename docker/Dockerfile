FROM python:3.10
ENV PYTHONUNBUFFERED=1
COPY requirements.txt /opt/hulahoop/
WORKDIR /opt/hulahoop/
RUN pip3 install --no-cache-dir -r requirements.txt \
    && rm -rf ~/.cache/ && rm -rf /tmp/*
COPY uwsgi /etc/uwsgi
COPY ../src /opt/hulahoop

#RUN python3 manage.py collectstatic --noinput

