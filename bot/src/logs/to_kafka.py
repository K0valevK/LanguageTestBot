from apscheduler.schedulers.background import BackgroundScheduler
from config import settings
from glob import glob
from os import remove
from logs.logger import new_file, log_names

from aiokafka import AIOKafkaProducer

import asyncio


scheduler = BackgroundScheduler()


async def send_one(topic: str, msg: str):
    producer = AIOKafkaProducer(
        bootstrap_servers=f"{settings.kafka_host}:{settings.kafka_port}")
    await producer.start()
    try:
        await producer.send_and_wait(topic, msg.encode("ascii"))
    finally:
        await producer.stop()


def send_user_journey():
    new_file(log_names["user_journey"])
    files = glob("./src/logs/log_files/_*-user_journey.tsv")
    for file in files:
        with open(file, 'r') as f:
            for line in f:
                asyncio.run(send_one("user_journey", line))
        remove(file)


def send_errors():
    new_file(log_names["errors"])
    files = glob("./src/logs/log_files/_*-errors.tsv")
    for file in files:
        with open(file, 'r') as f:
            for line in f:
                asyncio.run(send_one("errors", line))
        remove(file)


scheduler.add_job(send_user_journey, 'interval', minutes=2)
scheduler.add_job(send_errors, 'interval', minutes=2)
# scheduler.add_job(send_user_journey, 'interval', hours=24)
# scheduler.add_job(send_errors, 'interval', minutes=15)
