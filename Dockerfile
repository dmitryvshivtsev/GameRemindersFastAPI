FROM python:3.10

RUN mkdir -p /usr/src/FastAPI_trainee
COPY . /usr/src/FastAPI_trainee
WORKDIR /usr/src/FastAPI_trainee

CMD ["bash", "install.sh"]
