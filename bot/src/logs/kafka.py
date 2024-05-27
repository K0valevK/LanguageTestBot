from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiokafka import AIOKafkaProducer
from config import settings
from datetime import datetime
from glob import glob
from os import remove
from logs.logger import new_file, log_names, logging_format
from kafka_producer import kafka_producer, send_message


# scheduler = BackgroundScheduler()
scheduler = AsyncIOScheduler()


async def send_one(topic: str, msg: str, log_type: str):
    keys = logging_format[log_type].replace("{", "").replace("}", "").split()
    values = msg.split()

    data = dict(map(lambda i, j: (i, j), keys, values))
    tmp = datetime.strptime(data["timestamp"], "%Y-%m-%d-%H-%M-%S")
    data["timestamp"] = int(round(datetime.strptime(data["timestamp"], "%Y-%m-%d-%H-%M-%S").timestamp()))

    async with kafka_producer.session() as session:
        await send_message(session, topic, data)


async def send_user_journey():
    new_file(log_names["user_journey"])
    files = glob("./src/logs/log_files/_*-user_journey.tsv")
    for file in files:
        with open(file, 'r') as f:
            for line in f:
                await send_one("user_journey", line, "user_journey")
        remove(file)


async def send_errors():
    new_file(log_names["errors"])
    files = glob("./src/logs/log_files/_*-errors.tsv")
    for file in files:
        with open(file, 'r') as f:
            for line in f:
                await send_one("errors", line, "errors")
        remove(file)
