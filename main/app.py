import asyncio
import logging

from main.config import bot, dp

from handlers import start, admin, profile, order
from admin_menu.sendall import set_text, set_file_id, done, add_buttons
from admin_menu.product_add import add_prod, del_prod

logging.basicConfig(level=logging.INFO)


async def main():
    dp.include_routers(start.router, admin.router, set_text.router, set_file_id.router, add_buttons.router, done.router,
                       profile.router, order.router, add_prod.router, del_prod.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt or RuntimeError:
        print('Бот выключен')
