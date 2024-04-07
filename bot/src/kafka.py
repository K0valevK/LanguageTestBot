from aiokafka import AIOKafkaProducer
from config import settings

import contextlib
import json


class KafkaProducerSessionManager:
    def __init__(self, kafka_conf):
        self._kafka_conf = kafka_conf
        self._kafka_producer: AIOKafkaProducer = None

    async def init_producer(self):
        self._kafka_producer = AIOKafkaProducer(**self._kafka_conf)

    @contextlib.asynccontextmanager
    async def session(self):
        producer = self._kafka_producer
        if producer is None:
            raise Exception("Kafka producer is not initialized")

        try:
            await producer.start()
            yield producer
        finally:
            await producer.stop()


KAFKA_CONF = {"bootstrap_servers": f"{settings.kafka_host}:{settings.kafka_port}"}
kafka_producer = KafkaProducerSessionManager(KAFKA_CONF)


async def send_message(producer: AIOKafkaProducer, topic: str, value=None, key=None, headers=None):
    return await producer.send(topic, value.encode("ascii"), key=key, headers=headers)


async def get_kafka_producer():
    async with kafka_producer.session() as session:
        yield session
