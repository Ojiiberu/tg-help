from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from utils.data_loader import get_command_info, get_category,  get_all_categories, load_commands, random_command
from keyboards.button import main_buttons_kb, category_name, back_button

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
        reply_markup = category_name(cats, include_back=True)
        )
    await state.set_state(CategorySearch.waiting_for_category)


@router.message(CategorySearch.waiting_for_category, F.text.in_("назад"))
async def back_from_category(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Вы вернулись в главное меню", reply_markup=main_buttons_kb())
    
    
    
@router.message(CategorySearch.waiting_for_category)
async def show_category(message: Message, state: FSMContext):   
    text = message.text.strip()
    if text.lower() in ("назад"):
        await state.clear()
        await message.answer("Вы вернулись в главное меню", reply_markup=main_buttons_kb())
        return
    category = text
    commands = get_category(category)
    if not commands:
        cats = get_all_categories()
        await message.answer(
            "Категория не найдена или в ней нет команд.\n"
            "Выберите другую категорию или нажмите 'Назад' ",
            reply_markup=category_name(cats, include_back=True)
        )
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

    cats = get_all_categories()
    await message.answer(
        "Можете выбрать другую категорию или нажать 'Назад', чтобы вернуться в меню",
        reply_markup=category_name(cats, include_back=True)
    )
        

@router.message(F.text == "Поиск по имени")
async def ask_command_name(message: Message, state: FSMContext):
    await message.answer("Введите название команды или нажмите 'Назад' для выхода", reply_markup=back_button() )
    await state.set_state(CommandSearch.waiting_for_name)

@router.message(CommandSearch.waiting_for_name, F.text.in_("назад"))
async def back_from_name(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Вы вернулись в главное меню", reply_markup=main_buttons_kb())

@router.message(CommandSearch.waiting_for_name)
async def show_command_info(message: Message, state: FSMContext):
    text = message.text.strip()
    if text.lower() in ("назад"):
        await state.clear()
        await message.answer("Вы вернулись в главное меню", reply_markup=main_buttons_kb())
        return

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
    await message.answer(
        "Введите новую команду или нажмите 'Назад'",
        reply_markup=back_button()
    )

# @router.message(CategorySearch.waiting_for_category, F.text == "Назад")
# async def back_from_category(message: Message, state: FSMContext):
#     await state.clear()
#     await message.answer(
#         "Вы вернулись в главное меню",
#         reply_markup=main_buttons_kb()
#     )
# @router.message(CommandSearch.waiting_for_name, F.text == "назад")
# async def back_from_name(message: Message, state: FSMContext):
#     await state.clear()
#     await message.answer(
#         "Вы вернулись в главное меню",
#         reply_markup=main_buttons_kb()
#     )

@router.message(F.text == "Случайная команда")
async def random_command_show(message: Message):
    rand = random_command()
    if rand:
        await message.answer(
            f"Команда: {rand['name']}\n"
            f"Описание: {rand['description']}\n"
            f"Пример: {rand['example']}\n"
            f"Подробнее: {rand['link']}"
        )
    else:
        await message.answer("нет доступных команд")



# хелп