FROM python:3.11.4

COPY database/src/ /app/src/
COPY database/src/requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

ENV PYTHONPATH=/app
ENV DATABASE_TASK_URL="postgresql+asyncpg://postgres:postgres@postgresql:5432/task"
ENV DATABASE_STATISTIC_URL="postgresql+asyncpg://postgres:postgres@postgresql:5432/statistic"

ENTRYPOINT ["python3", "src/main.py"]