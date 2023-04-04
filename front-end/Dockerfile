FROM python:3.10.6-slim-buster

WORKDIR /app
COPY requirements.txt requirements.txt
ADD LiftSim LiftSim
COPY app.py app.py



RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt 


ENV FLASK_APP app.py

ENTRYPOINT [ "python", "-u", "-m", "flask", "run", "--host=0.0.0.0"]
