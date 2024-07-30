from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_menu_kb():
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text='Редактор товаров 🏷️', callback_data='red_prod_admin'),
        InlineKeyboardButton(text='Рассылка 📥', callback_data='in_sendall_admin'),
    )
    builder.row(
        InlineKeyboardButton(text='Назад ⬅️', callback_data='back_from_admin'),
    )

    return builder.as_markup()


def admin_menu_addprod_kb():
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text='Удалить товар 🗑️', callback_data='del_prod'),
        InlineKeyboardButton(text='Добавить товар 🛍️', callback_data='add_prod')
    )
    builder.row(
        InlineKeyboardButton(text='Назад ⬅️', callback_data='back_from_prod')
    )

    return builder.as_markup()


def admin_menu_sendall_kb():
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text='Установить текст 📝', callback_data='set_text'),
        InlineKeyboardButton(text='Установить файл 💾', callback_data='set_file')
    )
    builder.row(
        InlineKeyboardButton(text='Добавить кнопки 🎛️', callback_data='add_buttons'),
        InlineKeyboardButton(text='Готово ✅', callback_data='done')
    )
    builder.row(
        InlineKeyboardButton(text='Назад ⬅️', callback_data='back_from_sendall')
    )

    return builder.as_markup()


def del_file_keyboard():
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text='Удалить файл ❌ ', callback_data='del_file')
    )

    return builder.as_markup()


def del_buttons_keyboard():
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text='Удалить кнопку ❌', callback_data='delete_buttons')
    )

    return builder.as_markup()


def confirm_sendall():
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text='Уверен ✅', callback_data='yes_sendall')
    )
    builder.row(
        InlineKeyboardButton(text='Назад ⬅️', callback_data='back_to_admin')
    )

    return builder.as_markup()
