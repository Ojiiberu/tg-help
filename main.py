import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import questions
from aiogram.fsm.storage.memory import MemoryStorage

from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)


#загрузка данных из env
load_dotenv()
token = os.getenv("BOT_TOKEN")


async def main():
    bot = Bot(token=token)
    dp = Dispatcher(storage=MemoryStorage())


    dp.include_routers(questions.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
