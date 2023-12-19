#from python:3.11.4-alpine3.18
from python:3.11.4-bookworm

MAKEDIR /usr/src/website
COPY . /usr/src/website
RUN apt-get update -y
RUN apt-get install -y build-essential  mariadb-client libmariadbd-dev libffi-dev git
WORKDIR /usr/src/website
