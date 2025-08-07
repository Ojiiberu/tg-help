from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from utils.data_loader import get_command_info

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

class CommandSearch(StatesGroup):
    waiting_for_name = State()

@router.message(F.text == "Поиск по имени")
async def ask_command_name(message: Message, state: FSMContext):
    await message.answer("Введите название команды")
    await state.set_state(CommandSearch.waiting_for_name)


@router.message(CommandSearch.waiting_for_name)
async def show_command_info(message: Message, state: FSMContext):
    cmd = message.text.strip().lower()
    info = get_command_info(cmd)

    if info:
        await message.answer(
             f"🔹 Команда: {cmd}\n"
            f"📄 Описание: {info['description']}\n"
            f"🧪 Пример: {info['example']}\n"
            f"📚 Подробнее: {info['link']}"
        )
    else:
        await message.answer("Команда не найдена, попробуйте ещё раз")
    await state.clear()