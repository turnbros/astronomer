FROM ubuntu:focal

RUN apt-get update
RUN apt-get install -y make curl git python3 python3-pip python-is-python3

ADD . /code/astronomer/
WORKDIR /code/astronomer/

RUN /code/astronomer/download-helm-clients.sh
RUN cp /root/bin/helm /usr/local/bin/

RUN pip install virtualenv

CMD make unittest-charts
