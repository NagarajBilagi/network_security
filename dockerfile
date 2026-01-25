FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN apt-get update \
    && apt-get install -y awscli \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]