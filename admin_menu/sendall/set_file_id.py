from aiogram import Router, F

from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup

from database.viro_db import SessionLocal, Settings
from filters.isAdmin import IsAdmin

from keyboards.admin_menu_kb import del_file_keyboard

router = Router()


class SetFile(StatesGroup):
    setting_file = State()


@router.callback_query(IsAdmin(), StateFilter(None), F.data == 'set_file')
async def set_file_id(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Отправьте фото, видео или гиф', reply_markup=del_file_keyboard())
    await callback.answer()
    await state.set_state(SetFile.setting_file)


@router.message(IsAdmin(), SetFile.setting_file)
async def set_file(message: Message, state: FSMContext):
    photo = message.photo
    video = message.video
    animation = message.animation
    if photo:
        file_id = message.photo[0].file_id
    elif video:
        file_id = message.video.file_id
    elif animation:
        file_id = message.animation.file_id
    else:
        return
    await state.update_data(file=file_id)
    if photo:
        await message.answer_photo(file_id, caption='✅ Фото успешно добавлено!')
    elif video:
        await message.answer_video(file_id, caption='✅ Видео успешно добавлено!')
    elif animation:
        await message.answer_animation(file_id, caption='✅ Гифка успешно добавлена!')

    session = SessionLocal()
    settings = session.query(Settings).first()
    if settings:
        settings.file_id = file_id
    else:
        settings = Settings(file_id=file_id)
        session.add(settings)
    session.commit()
    session.close()

    await state.clear()


@router.callback_query(IsAdmin(), F.data == 'del_file')
async def del_file_id(callback: CallbackQuery):
    session = SessionLocal()
    settings = session.query(Settings).first()
    if settings:
        settings.file_id = None
        session.commit()
    session.close()
    await callback.message.answer('❌ Файл успешно удалён!')
    await callback.answer()
