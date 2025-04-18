FROM python:3.10-slim

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8011

CMD ["uvicorn", "backend.config.asgi:application", "--host", "0.0.0.0", "--port", "8011"]
