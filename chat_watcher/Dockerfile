FROM python:3.7-slim-stretch

WORKDIR /usr/local/chat_watcher

COPY . .

RUN pip3 install -r requirements.txt

# COPY main.py /usr/local/fake_chat_watcher

# CMD ["python", "main.py", "args", "go", "here", "when argparse is added ;)"]
CMD ["python","-u","bot.py"]
