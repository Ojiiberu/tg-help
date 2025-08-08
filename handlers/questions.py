from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from utils.data_loader import get_command_info, get_category,  get_all_categories, load_commands
from keyboards.button import main_buttons_kb, category_name

router = Router()  

@router.message(Command("start"))  
async def cmd_start(message: Message):
    await message.answer(
        "Привет!, вот основные мои команды:",
        reply_markup=main_buttons_kb()
    )

class CommandSearch(StatesGroup):
    waiting_for_name = State()
    

class CategorySearch(StatesGroup):
    waiting_for_category = State()

@router.message(F.text == "Категории")
async def ask_catigory_name(message: Message, state: FSMContext):
    cats = get_all_categories()
    if not cats:
        await message.answer("В базе нет ни одной категории")
        return
    await message.answer(
        text="Выберете интересующую категорию",
        reply_markup = category_name(cats)
        )
    await state.set_state(CategorySearch.waiting_for_category)


@router.message(CategorySearch.waiting_for_category)
async def show_category(message: Message, state: FSMContext):
    category = message.text.strip()
    commands = get_category(category)
    if not commands:
        try:
            all_cmds = load_commands()
            cats = sorted({(d.get("category") or "<нет категории>"). strip() for d in all_cmds.values()})
            await message.answer(
                f"DEBUG: Вы выбрали:'{category}'\n"
                f"Категории в базе: {cats}\n"
                f"Всего команд в базе: {len(all_cmds)}"
            )
        except Exception as e:
            await message.answer(f"DEBUG: Ошибка чтения базы: {e}")
        await message.answer("В этой категории пока нет команд")
        await state.clear()
        return
    
    lines = []
    for name, info in commands.items():
        desc = info.get("description", "-")
        example = info.get("example", "")
        link = info.get("link", "")
        lines.append(f"*{name}* - {desc}\n'{example}'\n{link}\n")
    
    def chunk_lines(lines, limit=3900):
        cur = ""
        for line in lines:
            if len(cur) + len(line) + 1 > limit:
                yield cur
                cur = line
            else:
                cur = cur + "\n" + line if cur else line
        if cur:
            yield cur
        
    for chunk in chunk_lines(lines):
        await message.answer(chunk, parse_mode="Markdown")
    await state.clear()
        

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