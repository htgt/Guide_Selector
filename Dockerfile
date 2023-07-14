FROM python:3.8.0

WORKDIR /app

COPY Makefile Makefile
RUN apt-get update
RUN make install

COPY requirements.txt requirements.txt
RUN make setup-venv

COPY src src
COPY tests tests

ENTRYPOINT ["python3", "src/cli.py"]
