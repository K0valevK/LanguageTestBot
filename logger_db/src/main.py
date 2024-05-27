from config import settings
from contextlib import asynccontextmanager
from fastapi import FastAPI
from kafka_consumer import kafka_uj_consumer, kafka_errors_consumer
from kafka_wrappers import uj_clickhouse_wrapper, errors_clickhouse_wrapper

import asyncio
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    await kafka_uj_consumer.init_consumer(settings.kafka_topic_uj, uj_clickhouse_wrapper)
    task = asyncio.create_task(kafka_uj_consumer.consume())

    await kafka_errors_consumer.init_consumer(settings.kafka_topic_errors, errors_clickhouse_wrapper)
    task2 = asyncio.create_task(kafka_errors_consumer.consume())

    yield
    await kafka_uj_consumer.stop()
    await kafka_errors_consumer.stop()


app = FastAPI(lifespan=lifespan, title=settings.project_name, docs_url="/docs")


if __name__ == '__main__':
    uvicorn.run("main:app", host=settings.me_host, port=settings.me_port, reload=True)
