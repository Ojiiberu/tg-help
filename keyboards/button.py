from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_buttons_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Категории")
    kb.button(text="Поиск по имени")
    kb.button(text="Поиск по описанию")
    kb.button(text="Случайная команда")
    kb.button(text="help")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

# def categories() -> ReplyKeyboardMarkup:
#     kb = ReplyKeyboardBuilder()
#     kb.button(text="Файлы и каталоги")
#     kb.button(text="Сеть")
#     kb.button(text="Процессы")
#     kb.button(text="Доступы и права")
#     kb.button(text="пакеты")
#     kb.button(text="Система и отчистка")
#     return kb.as_markup(resize_keyboard=True)
    