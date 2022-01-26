
FROM python:3.8-slim-buster

WORKDIR /usr/athena

COPY . .

RUN pip install --upgrade pip setuptools wheel --user

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

RUN pip install --no-cache-dir athena-0.1.0-py3-none-any.whl \
    && pip install --no-cache-dir numpy pandas

CMD ["python", "./test.py"]

# CMD ["python", "./new.py"]