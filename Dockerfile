FROM python:3.10.8-slim-bullseye

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

COPY . /usr/src/app/

EXPOSE 80

ENV TZ Europe/Moscow

CMD waitress-serve --host 0.0.0.0 --port 80 app:app