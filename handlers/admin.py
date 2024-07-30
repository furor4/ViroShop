from aiogram.types import CallbackQuery
from aiogram import Router, F

from filters.isAdmin import IsAdmin

from keyboards.admin_menu_kb import admin_menu_sendall_kb, admin_menu_kb, admin_menu_addprod_kb
from keyboards.start_kb import start_keyboard

router = Router()


@router.callback_query(IsAdmin(), F.data == 'admin')
async def admin(callback: CallbackQuery):
    await callback.message.edit_text('🛡️ Админ меню', reply_markup=admin_menu_kb())
    await callback.answer()


@router.callback_query(IsAdmin(), F.data == 'in_sendall_admin')
async def admin_sendall(callback: CallbackQuery):
    await callback.message.edit_text('🛡️ Админ меню: Рассылка', reply_markup=admin_menu_sendall_kb())
    await callback.answer()


@router.callback_query(IsAdmin(), F.data == 'red_prod_admin')
async def admin_addprod(callback: CallbackQuery):
    await callback.message.edit_text('🛡️ Админ меню: Добавление товаров', reply_markup=admin_menu_addprod_kb())
    await callback.answer()


@router.callback_query(F.data == 'admin')
async def not_admin(callback: CallbackQuery):
    await callback.answer('⛔️ У вас нет доступа к админ меню.', show_alert=True)


@router.callback_query(IsAdmin(), F.data == 'back_from_admin')
async def back_admin(callback: CallbackQuery):
    await callback.message.edit_text('Здравствуйте, вы пользуетесь ботом ViroShop. Прошу выбрать желаемое действие.',
                                     reply_markup=start_keyboard())
    await callback.answer()


@router.callback_query(IsAdmin(), F.data == 'back_from_sendall')
async def back_from_sendall(callback: CallbackQuery):
    await callback.message.edit_text('🛡️ Админ меню', reply_markup=admin_menu_kb())
    await callback.answer()


@router.callback_query(IsAdmin(), F.data == 'back_from_prod')
async def back_from_prod(callback: CallbackQuery):
    await callback.message.edit_text('🛡️ Админ меню', reply_markup=admin_menu_kb())
    await callback.answer()
