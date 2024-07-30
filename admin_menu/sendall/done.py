from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database.viro_db import SessionLocal, Settings, Keyboard, User
from filters.isAdmin import IsAdmin
from keyboards.admin_menu_kb import admin_menu_sendall_kb, confirm_sendall
from main.config import bot

router = Router()


@router.callback_query(IsAdmin(), F.data == 'done')
async def process_done(callback: CallbackQuery):
    await callback.message.answer("Вы уверены, что хотите отправить рассылку?", reply_markup=confirm_sendall())
    await callback.answer()


@router.callback_query(IsAdmin(), F.data == 'yes_sendall')
async def process_yes_sendall(callback: CallbackQuery):
    session = SessionLocal()
    try:
        settings = session.query(Settings).first()
        message_text = settings.send_text if settings else '❌ Нет текста для рассылки'
        file_id = settings.file_id if settings else None

        keyboards = session.query(Keyboard).all()
        inline_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=kb.text, url=kb.url)] for kb in keyboards
        ])

        users = session.query(User).all()

        for user in users:
            try:
                if file_id:
                    if file_id.startswith('photo'):
                        await bot.send_photo(user.user_id, file_id, caption=message_text, reply_markup=inline_kb)
                    elif file_id.startswith('video'):
                        await bot.send_video(user.user_id, file_id, caption=message_text, reply_markup=inline_kb)
                    elif file_id.startswith('animation'):
                        await bot.send_animation(user.user_id, file_id, caption=message_text, reply_markup=inline_kb)
                    else:
                        await bot.send_document(user.user_id, file_id, caption=message_text, reply_markup=inline_kb)
                else:
                    await bot.send_message(user.user_id, message_text, reply_markup=inline_kb)
            except Exception as e:
                print(f'Не удалось отправить сообщение пользователю {user.user_id}: {e}')

        await callback.message.answer('✅ Рассылка успешно завершена.')
        await callback.answer()

    finally:
        session.close()


@router.callback_query(IsAdmin(), F.data == 'back_to_admin')
async def admin(callback: CallbackQuery):
    await callback.message.edit_text('🛡️ Админ меню: Рассылка', reply_markup=admin_menu_sendall_kb())
    await callback.answer()


@router.callback_query(F.data == 'back_to_admin')
async def not_admin(callback: CallbackQuery):
    await callback.answer('⛔️ У вас нет доступа к админ меню.', show_alert=True)
