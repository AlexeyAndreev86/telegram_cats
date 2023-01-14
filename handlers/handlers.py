from aiogram import types, Dispatcher
from keyboard.keyboard import get_keyboard, get_one_button
from bot import bot
from random import choice
from db_postgres import DB
# from google_drive_api import GoogleDiskAPI


dp = Dispatcher(bot)
db = DB()
# disk = GoogleDiskAPI()


@dp.message_handler(commands='start')
async def start(message: types.Message):
    keyboard = get_keyboard()
    await message.answer('Кидай фотографию котика в чат или жми кнопку', reply_markup=keyboard)


@dp.message_handler()
async def reply(message: types.Message):
    keyboard = get_keyboard()
    await message.reply('Кидай фотографию котика в чат или жми кнопку', reply_markup=keyboard)


@dp.callback_query_handler(text='get_cat')
async def send_cat(call: types.CallbackQuery):
    chat = call.from_user.id
    keyboard = get_keyboard()

    # with open('file_id.txt', 'r') as file:
    #     photos = file.readlines()
    # images = [path.strip() for path in photos]
    # file_for_send = choice(images)

    db.cursor.execute('SELECT file_id FROM photos ORDER BY RANDOM() LIMIT 1;')
    file_for_send = db.cursor.fetchone()[0]

    await bot.send_photo(chat_id=chat, photo=file_for_send)
    await bot.send_message(chat_id=chat, text='Жми кнопку или кидай фото в чат', reply_markup=keyboard)

    @dp.callback_query_handler(text='how_many')
    async def cat_counter(call: types.CallbackQuery):
        chat = call.from_user.id
        keyboard = get_one_button()

        db.cursor.execute('SELECT COUNT(file_id) FROM photos;')
        count = db.cursor.fetchone()[0]

        await bot.send_message(chat_id=chat, text=f'У нас {count} котегов', reply_markup=keyboard)


@dp.message_handler(content_types=[types.ContentType.PHOTO])
async def echo_document(message: types.Message):
    """
    Пишем ID фотки в базу и в файл :)
    А хотелось писать в гугл диск.
    """
    id = message.photo[-1].file_id
    chat = message.from_user.id
    keyboard = get_keyboard()

    with open('file_id.txt', 'a') as f:
        f.write(id+'\n')

    db.cursor.execute(f"INSERT INTO photos (file_id) VALUES ('{id}');")
    db.connection.commit()
    await message.reply('Класс! Давай исчо!')
    await bot.send_message(chat_id=chat, text='Жми кнопку или кидай фото в чат', reply_markup=keyboard)
