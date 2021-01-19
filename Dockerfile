FROM ubuntu:20.04


RUN apt-get update
RUN apt-get install python3-dev python3-pip -y

COPY . /app
COPY requirements.txt /requirements.txt

ENV PYTHONPATH=/app

RUN pip3 install -r requirements.txt
WORKDIR /app

EXPOSE 8000

ENTRYPOINT ["uvicorn"]
CMD ["main:app", "--host", "0.0.0.0"]