import asyncio
from aiogram import types, Dispatcher
from keyboard.keyboard import get_keyboard, get_one_button
from bot import bot
from db_asyncpg import DB


dp = Dispatcher(bot)
db = DB()
loop = asyncio.get_event_loop()
loop.run_until_complete(db.create_pool())


@dp.message_handler()
@dp.message_handler(commands='start')
async def start(message: types.Message):
    keyboard = get_keyboard()
    await message.answer('Кидай фотографию котика в чат или жми кнопку', reply_markup=keyboard)


@dp.callback_query_handler(text='get_cat')
async def send_cat(call: types.CallbackQuery):
    chat = call.from_user.id
    keyboard = get_keyboard()

    file_for_send = await db.execute('SELECT file_id FROM photos ORDER BY RANDOM() LIMIT 1;', fetchval=True)

    if file_for_send is not None:
        await bot.send_photo(chat_id=chat, photo=file_for_send)
        await bot.send_message(chat_id=chat, text='Жми кнопку или кидай фото в чат', reply_markup=keyboard)
    else:
        await bot.send_message(chat_id=chat, text='У нас пока нет котегов :(')


@dp.callback_query_handler(text='how_many')
async def cat_counter(call: types.CallbackQuery):
    chat = call.from_user.id
    keyboard = get_one_button()

    count = await db.execute('SELECT COUNT(file_id) FROM photos;', fetchval=True)
    await bot.send_message(chat_id=chat, text=f'У нас {count} котегов', reply_markup=keyboard)


@dp.message_handler(content_types=[types.ContentType.PHOTO])
async def write_photo_id_into_postgres(message: types.Message):
    photo_id = message.photo[-1].file_id
    chat = message.from_user.id
    keyboard = get_keyboard()

    await db.execute(f"INSERT INTO photos (file_id) VALUES ('{photo_id}');", fetch=True)
    await message.reply('Класс! Давай исчо!')
    await bot.send_message(chat_id=chat, text='Жми кнопку или кидай фото в чат', reply_markup=keyboard)
