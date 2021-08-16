FROM ubuntu:focal

RUN apt-get update
RUN apt-get install -y make curl git python3 python3-pip python-is-python3
RUN pip install virtualenv

COPY download-helm-clients.sh /usr/local/bin/
RUN /usr/local/bin/download-helm-clients.sh
RUN cp /root/bin/helm /usr/local/bin/

ADD . /code/astronomer/
WORKDIR /code/astronomer/

CMD make unittest-charts
