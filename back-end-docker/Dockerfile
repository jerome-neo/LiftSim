FROM python:3.10.6-slim-buster

## Add Python script, requirements file and templates folder to /app 
## directory on the image:

WORKDIR /app
COPY back-end-docker/requirements.txt requirements.txt
COPY back-end-docker/API.py API.py
COPY src src

RUN pip install --upgrade pip
RUN pip install -r requirements.txt 

## Set the environment variable for the flask application here:
ENV FLASK_APP API.py
ENTRYPOINT ["python", "-u", "-m", "flask", "run", "--host=0.0.0.0"]
