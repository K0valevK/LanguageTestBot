FROM python:3.11.4

COPY database/src/ /app/src/
COPY database/src/requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

ENV PYTHONPATH=/app
ENV DATABASE_URL="postgresql+asyncpg://postgres:postgres@fintech-postgresql:5432/database"

ENTRYPOINT ["python3", "src/main.py"]