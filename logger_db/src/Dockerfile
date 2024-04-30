FROM python:3.11.4

COPY logger_db/src/ /app/src/
COPY logger_db/src/requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

ENV PYTHONPATH=/app
ENV KAFKA_HOST="kafka"
ENV KAFKA_PORT=29092
ENV CH_HOST="clickhouse"
ENV CH_PORT=9000

ENTRYPOINT ["python", "src/main.py"]
