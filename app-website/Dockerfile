#from python:3.11.4-alpine3.18
from python:3.11.4-bookworm


COPY ./www /usr/src/website/
COPY ./start.sh /start.sh
RUN apt-get update -y
RUN apt-get install -y build-essential  mariadb-client libmariadbd-dev libffi-dev git
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
WORKDIR /usr/src/website
