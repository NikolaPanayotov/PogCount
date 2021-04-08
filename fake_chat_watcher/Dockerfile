FROM python:3.7-slim-stretch

WORKDIR /usr/local/fake_chat_watcher

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY main.py /usr/local/fake_chat_watcher

# CMD ["python", "main.py", "args", "go", "here", "when argparse is added ;)"]
CMD ["python","-u","main.py"]