from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from aiogram import Router, F

from keyboards.profile_kb import add_balance, back_to_profile
from database.viro_db import SessionLocal, User
from keyboards.start_kb import start_keyboard

router = Router()


class AddBalance(StatesGroup):
    adding_balance = State()
    withdrawing_balance = State()


@router.callback_query(F.data == 'profile')
async def profile(callback: CallbackQuery):
    user_id = callback.from_user.id

    session = SessionLocal()
    user = session.query(User).filter(User.user_id == user_id).first()

    if user:
        profile_text = (
            f'👤 Профиль пользователя:\n'
            f'ID: {callback.from_user.id}\n'
            f'Юзернейм: @{callback.from_user.username}\n\n'
            f'💵 Баланс: {user.balance}₽'
        )
    else:
        profile_text = '❌ Профиль пользователя не найден'

    await callback.answer()
    await callback.message.edit_text(profile_text, reply_markup=add_balance())


@router.callback_query(StateFilter(None), F.data == 'add_balance')
async def add_amount(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text('Введите сумму для пополнения баланса.\nПример: 1500')
    await state.set_state(AddBalance.adding_balance)


@router.message(AddBalance.adding_balance)
async def process_add_amount(message: Message, state: FSMContext):
    try:
        amount = int(message.text)
        if amount <= 0:
            raise ValueError('Amount must be positive.')

        user_id = message.from_user.id
        session = SessionLocal()
        user = session.query(User).filter(User.user_id == user_id).first()

        if user:
            user.balance += amount
            session.commit()
            await message.answer(f'✅ Ваш баланс был успешно пополнен на {amount}₽!\n\nТекущий баланс: {user.balance}₽',
                                 reply_markup=back_to_profile())
        else:
            await message.answer('❌ Профиль пользователя не найден')
    except ValueError:
        await message.answer('❌ Сумма пополнения должна быть выше нуля.')

    await state.clear()


@router.callback_query(StateFilter(None), F.data == 'withdraw_balance')
async def withdraw_amount(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    session = SessionLocal()
    user = session.query(User).filter(User.user_id == user_id).first()

    if user:
        await callback.answer()
        await callback.message.edit_text(f'Введите сумму для снятия с баланса.\nПример: 1500\n\nТекущий баланс:'
                                         f' {user.balance}₽')
        await state.set_state(AddBalance.withdrawing_balance)
    else:
        await callback.answer('❌ Профиль пользователя не найден')


@router.message(AddBalance.withdrawing_balance)
async def process_withdraw_amount(message: Message, state: FSMContext):
    try:
        amount = int(message.text)
        if amount <= 0:
            raise ValueError('Amount must be positive.')

        user_id = message.from_user.id
        session = SessionLocal()
        user = session.query(User).filter(User.user_id == user_id).first()

        if user:
            if user.balance >= amount:
                user.balance -= amount
                session.commit()
                await message.answer(f'✅ Вы успешно обналичили {amount}₽!\n\nТекущий баланс: {user.balance}₽',
                                     reply_markup=back_to_profile())
            else:
                await message.answer('❌ Недостаточно средств на балансе.', reply_markup=back_to_profile())
        else:
            await message.answer('❌ Профиль пользователя не найден')
    except ValueError:
        await message.answer('❌ Сумма пополнения должна быть выше нуля.', reply_markup=back_to_profile())
    await state.clear()


@router.callback_query(F.data == 'back_to_start')
async def to_start(callback: CallbackQuery):
    await callback.message.edit_text('Здравствуйте, вы пользуетесь ботом ViroShop. Прошу выбрать желаемое действие.',
                                     reply_markup=start_keyboard())
    await callback.answer()


@router.callback_query(F.data == 'back_to_profile')
async def to_profile(callback: CallbackQuery):
    user_id = callback.from_user.id

    session = SessionLocal()
    user = session.query(User).filter(User.user_id == user_id).first()
    if user:
        profile_text = (
            f'👤 Профиль пользователя:\n'
            f'ID: {callback.from_user.id}\n'
            f'Юзернейм: @{callback.from_user.username}\n\n'
            f'💵 Баланс: {user.balance}₽'
        )
    else:
        profile_text = '❌ Профиль пользователя не найден'
    await callback.answer()
    await callback.message.edit_text(profile_text, reply_markup=add_balance())
