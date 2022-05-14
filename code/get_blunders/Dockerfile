FROM ubuntu:20.04

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN apt-get update \
    && apt-get install -y python3-pip \
    && apt install -y gunicorn \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && apt install -y nodejs \
    && apt install -y npm \
    && npm install -g analyze-sgf \
    && apt install -y libzip-dev \
    && apt-get install -y lsb-core \
    && python3 -m pip install --no-cache-dir -r requirements.txt


COPY katago /katago
COPY /katago/.analyze-sgf.yml /home/.analyze-sgf.yml
COPY /katago/.analyze-sgf.yml /root/.analyze-sgf.yml


#CMD exec /bin/bash
CMD exec gunicorn3 --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app