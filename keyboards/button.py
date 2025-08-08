from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from typing import Iterable


def main_buttons_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Категории")
    kb.button(text="Поиск по имени")
    kb.button(text="Случайная команда")
    kb.button(text="help")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def category_name(categories: Iterable[str]) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    buttons = [KeyboardButton(text=c) for c in categories]
    kb.add(*buttons)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)