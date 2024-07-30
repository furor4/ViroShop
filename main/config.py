from aiogram import Bot, Dispatcher
from environs import Env
from aiogram.fsm.storage.memory import MemoryStorage

env = Env()
env.read_env('info.env')  # Вставьте в файл .env ID своих администраторов

TOKEN = env.str('TOKEN')
ADMIN_VIR = env.int('ADMIN_VIR')
ADMIN_YEM = env.int('ADMIN_YEM')
bot = Bot(token=TOKEN)

dp = Dispatcher(storage=MemoryStorage())