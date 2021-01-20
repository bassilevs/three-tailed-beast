FROM ubuntu:20.04
RUN apt-get update
RUN apt-get install python3-dev python3-pip -y

COPY ./api /api/api
COPY requirements.txt /requirements.txt

ENV PYTHONPATH=/aoi

RUN pip3 install -r requirements.txt
WORKDIR /api

EXPOSE 8000

ENTRYPOINT ["uvicorn"]
CMD ["api.main:app", "--host", "0.0.0.0"]