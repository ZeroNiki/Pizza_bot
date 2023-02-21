from aiogram.utils import executor
from create_bot import dp
from script import clientP, admin, other
from data_base import sqlite_db


async def on_startup(_):
    print('Бот вышел в онлайн')
    sqlite_db.sql_start()


clientP.register_script_client(dp)
admin.register_handler_admin(dp)
other.register_script_other(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
