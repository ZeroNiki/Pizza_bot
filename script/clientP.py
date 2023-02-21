from aiogram import types
from create_bot import dp, bot, Dispatcher
from keyboards import kb_client
from aiogram.types import ReplyKeyboardRemove
from data_base import sqlite_db


# @dp.message_handler(commands=['start', 'help'])
async def commands_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Приятного аппетита', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите боту:\nt.me/MocorellaBot')


# @dp.message_handler(commands=['Режим_работы'])
async def pizza_open(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вт-Чт с 9.00 до 20.00, Пт-Сб с 10.00 до 23.00')


# @dp.message_handler(commands=['Расположение'])
async def pizza_place(message: types.Message):
    await bot.send_message(message.from_user.id, 'Ул. Пушкина 6')


# Menu
async def pizza_menu_command(message: types.Message):
    await sqlite_db.sql_read(message)


def register_script_client(dp: Dispatcher):
    dp.register_message_handler(commands_start, commands=['start', 'help'])
    dp.register_message_handler(pizza_open, commands=['Режим_работы'])
    dp.register_message_handler(pizza_place, commands=['Расположение'])
    dp.register_message_handler(pizza_menu_command, commands=['Меню'])
