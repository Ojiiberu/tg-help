import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)


#загрузка данных из env
load_dotenv()
token = os.getenv("BOT_TOKEN")

#Объект бота
bot = Bot(token=token)

#Диспетчер
dp = Dispatcher()

#Хендлер /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")

@dp.message(Command("test1"))
async def cmd_test1(message: types.Message):
    await message.reply("Test 1")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

