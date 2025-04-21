FROM python:3.9

WORKDIR /app

RUN apt-get update && \
    apt-get install -y gcc python3-dev libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY auth_app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY auth_app/ .

ENV PYTHONPATH=/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]