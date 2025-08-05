from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.button import main_buttons_kb, categories

router = Router()  

@router.message(Command("start"))  
async def cmd_start(message: Message):
    await message.answer(
        "Привет!, вот основные мои команды:",
        reply_markup=main_buttons_kb()
    )

@router.message(F.text.lower() == "Категории")
async def answer_yes(message: Message):
    await message.answer(
        "Какая категория вас интересует",
        reply_markup=categories()
    )

@router.message(F.text.lower() == "Поиск по имени")
async def answer_no(message: Message):
    await message.answer(
        "Введите команду.",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(F.text.lower() == "Поиск по описанию")
async def answer_no(message: Message):
    await message.answer(
        "Введите ключевое слово",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(F.text.lower() == "Случайная команда")
async def answer_no(message: Message):
    await message.answer(
        "Вывод случайной комады",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(F.text.lower() == "help")
async def answer_no(message: Message):
    await message.answer(
        "Вывод полезной информации",
        reply_markup=ReplyKeyboardRemove()
    )