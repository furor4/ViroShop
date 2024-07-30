from aiogram import Router, F

from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup

from database.viro_db import SessionLocal, Products
from filters.isAdmin import IsAdmin

router = Router()


class AddProducts(StatesGroup):
    waiting_name = State()
    waiting_description = State()
    waiting_price = State()


@router.callback_query(IsAdmin(), StateFilter(None), F.data == 'add_prod')
async def add_product(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите наименование нового товара.')
    await state.set_state(AddProducts.waiting_name)
    await callback.answer()


@router.message(AddProducts.waiting_name)
async def process_prod_name(message: Message, state: FSMContext):
    product_name = message.text.strip()
    await state.update_data(name=product_name)
    await message.answer('Введите описание нового товара.')
    await state.set_state(AddProducts.waiting_description)


@router.message(AddProducts.waiting_description)
async def process_prod_desc(message: Message, state: FSMContext):
    product_desc = message.text.strip()
    await state.update_data(description=product_desc)
    await message.answer('Введите цену нового товара. Пример: 100.0')
    await state.set_state(AddProducts.waiting_price)


@router.message(AddProducts.waiting_price)
async def process_prod_price(message: Message, state: FSMContext):
    try:
        product_price = message.text.strip()
        await state.update_data(price=product_price)

        data = await state.get_data()
        product_name = data['name']
        product_desc = data['description']
        product_price = data['price']

        new_product = Products(name=product_name, description=product_desc, price=product_price)
        session = SessionLocal()
        session.add(new_product)
        session.commit()

        await message.answer(f'✅ Товар "{product_name}" успешно добавлен в базу данных!')
        await state.clear()

    except ValueError:
        await message.answer('❌ Некорректное значение цены. Пример: 100.0')
