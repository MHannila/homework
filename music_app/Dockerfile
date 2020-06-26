FROM tiangolo/uwsgi-nginx-flask:latest

RUN apt-get update -y && \
    apt-get install -y apt-utils python3-pip

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "src/api.py" ]