from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def order_pagination(page: int, total_products: int, items_per_page: int):
    builder = InlineKeyboardBuilder()

    total_pages = (total_products + items_per_page - 1) // items_per_page

    builder.row(
        InlineKeyboardButton(text='Купить 💸', callback_data='buy_order')
    )

    if page > 1:
        builder.row(
            InlineKeyboardButton(text='⬅️ Назад', callback_data=f'order_page_{page - 1}')
        )

    if page < total_pages:
        builder.row(
            InlineKeyboardButton(text='Вперёд ➡️', callback_data=f'order_page_{page + 1}')
        )

    builder.row(
        InlineKeyboardButton(text=f'Страница {page}/{total_pages}', callback_data='ignore')
    )
    builder.row(
        InlineKeyboardButton(text='На главную ↩️', callback_data='back_from_orders')
    )

    return builder.as_markup()
