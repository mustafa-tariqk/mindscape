#use the offically supported node.js base image
FROM python:3.10

ENV REACT_APP_API_BASE_URL: http://localhost:<change>

ENV PORT = 8080

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD flask run --host=0.0.0.0