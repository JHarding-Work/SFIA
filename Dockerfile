FROM python:3.11
RUN apt-get update && apt-get install -y python3-pip
COPY app .
COPY requirements.txt .
RUN pip3 install -r requirements.txt
EXPOSE 5000
ENTRYPOINT python3 app.py