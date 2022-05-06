FROM ubuntu:20.04

RUN apt-get update && apt-get install -y python3
RUN apt-get install -y python3-pip
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt install -y nodejs
RUN apt install -y npm


RUN npm install -g analyze-sgf

COPY katago /katago
COPY .analyze-sgf.yml /root/.analyze-sgf.yml
COPY .analyze-sgf.yml /root/.analyze-sgf.yml
COPY test_in /
COPY test_out /
RUN apt install -y git
RUN git clone https://Holidin:R6t4r6t4@workshop.samcs.ru/bitbucket/scm/gopl/go-player-level.git
RUN apt install -y libzip-dev
RUN apt-get install -y lsb-core
RUN ./katago/katago benchmark

RUN python3 -m pip install tensorflow
RUN python3 -m pip install numpy
RUN python3 -m pip install catboost
RUN python3 -m pip install sklearn
RUN python3 -m pip install pandas
RUN python3 -m pip install tqdm
RUN python3 -m pip install scipy