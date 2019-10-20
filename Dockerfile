FROM python:3.7-slim-buster

RUN mkdir /app
WORKDIR /app
COPY requirements.txt requirements.txt
RUN apt update && apt install -y build-essential libssl-dev libffi-dev libgtk-3-dev python3-pyqt5 pyqt5-dev-tools libnss3 libasound2-dev 
RUN pip install -r requirements.txt
COPY . /app/
ENV BG_DOCKERENV=1
ENTRYPOINT [ "python3" ]
CMD ["app.py"]

