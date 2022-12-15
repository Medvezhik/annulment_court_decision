FROM python:3.8.15-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY predictor predictor
ENTRYPOINT ["python", "-m", "predictor.main"]
