from aiogram.types import Message
from aiogram.filters import BaseFilter

from main.config import ADMIN_YEM, ADMIN_VIR


class IsAdmin(BaseFilter):
    def __init__(self) -> None:
        self.admins_list = [ADMIN_YEM, ADMIN_VIR]

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admins_list
