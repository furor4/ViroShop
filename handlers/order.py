from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from database.viro_db import Products, SessionLocal, User
from keyboards.order_kb import order_pagination
from keyboards.profile_kb import back_to_profile
from keyboards.start_kb import start_keyboard

router = Router()

ITEMS_PER_PAGE = 5


class OrderBuy(StatesGroup):
    waiting_prod_number = State()


def get_product_by_number(session, product_number, items_per_page):
    offset = (product_number - 1) // items_per_page * items_per_page
    products = session.query(Products).offset(offset).limit(items_per_page).all()
    index_within_page = (product_number - 1) % items_per_page

    if index_within_page < len(products):
        return products[index_within_page]
    return None


@router.callback_query(F.data == 'order')
async def show_products(callback: CallbackQuery):
    await show_product_page(callback, page=1)
    await callback.answer()


async def show_product_page(callback: CallbackQuery, page: int):
    session = SessionLocal()
    try:
        products = session.query(Products).offset((page - 1) * ITEMS_PER_PAGE).limit(ITEMS_PER_PAGE).all()
        total_products = session.query(Products).count()

        if not products:
            await callback.message.answer('Ассортимент пуст.')
            return

        text = '🛍️ Наш ассортимент:\n\n'
        start_index = (page - 1) * ITEMS_PER_PAGE + 1
        for index, product in enumerate(products, start=start_index):
            text += f'{index}. 📦 {product.name}\n{product.description}\n💵 Цена: {product.price}₽\n\n'

        pagination_kb = order_pagination(page, total_products, ITEMS_PER_PAGE)

        if callback.message:
            await callback.message.edit_text(text, reply_markup=pagination_kb)
        else:
            await callback.message.answer(text, reply_markup=pagination_kb)

    finally:
        session.close()


@router.callback_query(F.data.startswith('order_page_'))
async def paginate_product(callback: CallbackQuery):
    page = int(callback.data.split('_')[-1])
    await show_product_page(callback, page)
    await callback.answer()


@router.callback_query(F.data == 'buy_order')
async def ask_for_number_prod(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите номер товара, который вы желаете приобрести.')
    await state.set_state(OrderBuy.waiting_prod_number)
    await callback.answer()


@router.message(OrderBuy.waiting_prod_number)
async def process_number_prod(message: Message, state: FSMContext):
    session = SessionLocal()
    try:
        product_number = int(message.text)
        user_id = message.from_user.id
        user = session.query(User).filter(User.user_id == user_id).first()
        product = get_product_by_number(session, product_number, ITEMS_PER_PAGE)

        if not product:
            await message.answer('❌ Товар с указанным номером не найден. Проверьте номер товара.')
        elif user.balance < product.price:
            await message.answer('❌ Недостаточно средств для приобретения данного товара. Пополните баланс.')
        else:
            user.balance -= product.price
            session.commit()
            await message.answer(f'✅ Товар "{product.name}" был успешно приобретён за {product.price}₽!\n\n'
                                 f'Текущий баланс: {user.balance}₽', reply_markup=back_to_profile())
    except ValueError:
        await message.answer('❌ Товар с указанным номером не найден. Проверьте номер товара.')
    finally:
        session.close()

    await state.clear()


@router.callback_query(F.data == 'back_from_orders')
async def back_from_orders(callback: CallbackQuery):
    await callback.message.edit_text('Здравствуйте, вы пользуетесь ботом ViroShop. Прошу выбрать желаемое действие.',
                                     reply_markup=start_keyboard())
    await callback.answer()


@router.callback_query(F.data == 'ignore')
async def ignore_product(callback: CallbackQuery):
    await callback.answer()
