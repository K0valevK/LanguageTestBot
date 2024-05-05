FROM python:3.11.4

COPY bot/src/ app/src/
COPY bot/src/requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

ENV PYTHONPATH=/app
ENV MODE="release"
ENV DATABASE_HOST="database"
ENV DATABASE_PORT=8000
ENV KAFKA_HOST="kafka"
ENV KAFKA_PORT=29092

ENTRYPOINT ["python3", "src/main.py"]