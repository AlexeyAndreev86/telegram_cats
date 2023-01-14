from aiogram import types, Dispatcher
from keyboard.keyboard import get_keyboard, get_one_button
from bot import bot
from random import choice

dp = Dispatcher(bot)


@dp.message_handler()
@dp.message_handler(commands='start')
async def start(message: types.Message):
    keyboard = get_keyboard()
    await message.answer('Кидай фотографию котика в чат или жми кнопку', reply_markup=keyboard)


@dp.callback_query_handler(text='get_cat')
async def send_cat(call: types.CallbackQuery):
    chat = call.from_user.id
    keyboard = get_keyboard()

    with open('file_id.txt', 'r') as file:
        photos = file.readlines()
    images = [path.strip() for path in photos]
    if len(images) > 0:
        file_for_send = choice(images)
        await bot.send_photo(chat_id=chat, photo=file_for_send)
        await bot.send_message(chat_id=chat, text='Жми кнопку или кидай фото в чат', reply_markup=keyboard)
    else:
        await bot.send_message(chat_id=chat, text='У нас пока нет котегов :(')

    @dp.callback_query_handler(text='how_many')
    async def cat_counter(call: types.CallbackQuery):
        chat = call.from_user.id
        keyboard = get_one_button()

        with open('file_id.txt', 'r') as file:
            photos = file.readlines()
        count = len([path.strip() for path in photos])

        await bot.send_message(chat_id=chat, text=f'У нас {count} котегов', reply_markup=keyboard)


@dp.message_handler(content_types=[types.ContentType.PHOTO])
async def echo_document(message: types.Message):

    id = message.photo[-1].file_id
    chat = message.from_user.id
    keyboard = get_keyboard()

    with open('file_id.txt', 'a') as f:
        f.write(id+'\n')

    await message.reply('Класс! Давай исчо!')
    await bot.send_message(chat_id=chat, text='Жми кнопку или кидай фото в чат', reply_markup=keyboard)
