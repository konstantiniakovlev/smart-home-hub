FROM --platform=linux/arm/v8 python:3.11 as build
LABEL authors="Konstantin"

COPY src/. src/.
COPY requirements.txt .
COPY .env .

ENV POSTGRES_HOST=host.docker.internal

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["python", "src/api/main.py"]
