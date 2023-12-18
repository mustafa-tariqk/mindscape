#use the offically supported node.js base image
FROM python:3.10

ENV REACT_APP_API_BASE_URL: http://localhost:<change>

ENV PORT = 5000

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "flask -app app run" ]