#use the offically supported node.js base image
FROM python:3.10

ENV PORT=8080

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD gunicorn --bind 0.0.0.0:8080 --timeout 0 app:app