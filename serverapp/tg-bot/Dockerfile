FROM python:3.8.15-alpine3.16

RUN apk add antiword
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY tg_bot tg_bot
ENTRYPOINT ["python", "-m", "tg_bot"]
