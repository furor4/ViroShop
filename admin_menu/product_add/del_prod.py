from aiogram import Router, F

from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup

from database.viro_db import SessionLocal, Products
from filters.isAdmin import IsAdmin

router = Router()


class ProductDel(StatesGroup):
    waiting_number = State()


@router.callback_query(IsAdmin(), StateFilter(None), F.data == 'del_prod')
async def del_prod_cb(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите номер товара, который хотите удалить.')
    await callback.answer()
    await state.set_state(ProductDel.waiting_number)


@router.message(IsAdmin(), ProductDel.waiting_number)
async def complete_del_prod_cb(message: Message, state: FSMContext):
    try:
        product_number = int(message.text)
        session = SessionLocal()
        products = session.query(Products).all()

        if product_number < 1 or product_number > len(products):
            await message.answer('❌ Некорректный номер товара. Проверьте номер товара, который хотите удалить.')
            return

        product_to_del = products[product_number - 1]
        session.delete(product_to_del)
        session.commit()

        await message.answer(f'✅ Товар "{product_to_del.name}" успешно удалён!')
        await state.clear()

    except ValueError:
        await message.answer('❌ Некорректный номер товара. Проверьте номер товара, который хотите удалить.')
    except Exception as e:
        await message.answer('❌ Произошла ошибка при удалении товара. Попробуйте позже.')
