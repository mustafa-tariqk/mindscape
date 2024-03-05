FROM python:3.10

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE ${SERVER_PORT}

CMD if [ "$TESTING" = "0" ]; then \
    gunicorn --bind 0.0.0.0:${SERVER_PORT} \
    --certfile=fullchain.pem \
    --keyfile=privkey.pem \
    --timeout 0 app:app; \
else \
    gunicorn --bind 0.0.0.0:${SERVER_PORT} \
    --timeout 0 app:app; \
fi