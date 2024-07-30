from aiogram import Router

from aiogram.filters import CommandStart
from aiogram.types import Message

from database.viro_db import SessionLocal, User
from keyboards.start_kb import start_keyboard

router = Router()


@router.message(CommandStart())
async def start_bot(message: Message):
    user_id = message.from_user.id
    user_username = message.from_user.username
    user_full_name = message.from_user.full_name

    session = SessionLocal()
    user = session.query(User).filter(User.user_id == user_id).first()

    if not user:
        user = User(user_id=user_id, username=user_username, full_name=user_full_name, balance=0)
        session.add(user)
        session.commit()
    await message.answer('Здравствуйте, вы пользуетесь ботом ViroShop. Прошу выбрать желаемое действие.',
                         reply_markup=start_keyboard())