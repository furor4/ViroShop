from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def add_balance():
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text='Обналичить деньги 💰', callback_data='withdraw_balance'),
        InlineKeyboardButton(text='Пополнить баланс 💰', callback_data='add_balance')
    )

    builder.row(
        InlineKeyboardButton(text='Назад ⬅️', callback_data='back_to_start'),
    )

    return builder.as_markup()


def back_to_profile():
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text='Назад ⬅️', callback_data='back_to_profile')
    )

    return builder.as_markup()
