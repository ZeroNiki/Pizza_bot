from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards import admin_kb
from create_bot import dp, bot


class FSMadmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


# Начало диалога загрузки нового пункта меню
async def cm_start(message: types.Message):
    await FSMadmin.photo.set()
    await message.reply('Загрузи фото')


# выход из состояния
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Ok')


# Принимаем первый ответ и пишем в словарь
async def load_photo(message: types.Message, state: FSMadmin):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMadmin.next()
    await message.reply('Теперь введите название')


# Принимаем второй ответ
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMadmin.next()
    await message.reply('Введи описание')


# Принимаем третий ответ
async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMadmin.next()
    await message.reply("Теперь укажи цену")


# Принимаем четвертый ответ и используем полученные данные
async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = float(message.text)
    await sqlite_db.sql_add_command(state)
    await state.finish()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена.', show_alert=True)


@dp.message_handler(commands='Удалить')
async def delete_item(message: types.Message):
    read = await sqlite_db.sql_read2()
    for ret in read:
        await  bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена: {ret[-1]}')
        await bot.send_message(message.from_user.id, text='^^^',
                               reply_markup=InlineKeyboardMarkup().add(
                                   InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))


# Регистрируем хендлеры
def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMadmin.photo)
    dp.register_message_handler(load_name, state=FSMadmin.name)
    dp.register_message_handler(load_description, state=FSMadmin.description)
    dp.register_message_handler(load_price, state=FSMadmin.price)
