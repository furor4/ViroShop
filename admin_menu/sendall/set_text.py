from aiogram import Router, F

from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup

from database.viro_db import SessionLocal, Settings
from filters.isAdmin import IsAdmin

router = Router()


class SetText(StatesGroup):
    writing_text = State()


@router.callback_query(IsAdmin(), StateFilter(None), F.data == 'set_text')
async def set_text(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите желаемый текст рассылки.')
    await callback.answer()
    await state.set_state(SetText.writing_text)


@router.message(IsAdmin(), SetText.writing_text)
async def write_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    user_data = await state.get_data()
    await message.answer(f'✅ Текст рассылки успешно установлен!\n\n{user_data["text"]}')

    session = SessionLocal()
    settings = session.query(Settings).first()
    if settings:
        settings.send_text = user_data["text"]
    else:
        settings = Settings(send_text=user_data["text"])
        session.add(settings)
    session.commit()
    session.close()

    await state.clear()