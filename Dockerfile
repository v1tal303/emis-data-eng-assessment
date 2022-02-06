FROM python:3.10

WORKDIR /app

COPY requirements.txt .

COPY ./data ./data

RUN pip install -r requirements.txt

COPY ./app ./app

CMD ["python", "./app/main.py"]