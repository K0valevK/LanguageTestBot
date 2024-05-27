from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from config import settings
from logs import scheduler, send_errors, send_user_journey
from kafka_producer import kafka_producer

import asyncio
import handlers
import logging


async def main():
    await kafka_producer.init_producer()

    if settings.mode == "debug":
        scheduler.add_job(send_user_journey, 'interval', minutes=2)
        scheduler.add_job(send_errors, 'interval', minutes=2)
    else:
        scheduler.add_job(send_user_journey, 'interval', hours=24)
        scheduler.add_job(send_errors, 'interval', minutes=15)
    scheduler.start()

    bot = Bot(token=settings.bot_token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(handlers.test_router)
    dp.include_router(handlers.statistics_router)
    dp.include_router(handlers.start_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
