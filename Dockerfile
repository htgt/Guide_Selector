FROM python:3.8.0

WORKDIR /app

COPY Makefile Makefile

RUN apt-get update
RUN make install

COPY requirements.txt requirements.txt
COPY td_utils/requirements.txt td_utils/requirements.txt
RUN make setup-venv

COPY td_utils/tdutils td_utils/tdutils
COPY src src
COPY tests tests
