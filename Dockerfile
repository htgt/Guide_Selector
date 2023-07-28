FROM python:3.8.0

WORKDIR /app

COPY Makefile Makefile
COPY requirements.txt requirements.txt
COPY td_utils/requirements.txt td_utils/requirements.txt
COPY td_utils/tdutils td_utils/tdutils
COPY src src
COPY tests tests

RUN apt-get update

RUN make install
RUN make setup-venv
