from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def start_keyboard():
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text='Профиль 👤', callback_data='profile'),
        InlineKeyboardButton(text='Заказать 🛒', callback_data='order')
    )
    builder.row(
        InlineKeyboardButton(text='Админ 🔰', callback_data='admin')
    )

    return builder.as_markup()