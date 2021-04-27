FROM python:3.7-slim-stretch

WORKDIR /usr/local/migrator

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY * /usr/local/migrator

CMD ["python","-u","migrator.py"]