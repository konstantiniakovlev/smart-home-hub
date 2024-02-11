FROM --platform=linux/arm/v8 python:3.9 as build
LABEL authors="Konstantin"

COPY config/. config/.
COPY src/. src/.
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["python", "src/app/main.py"]
