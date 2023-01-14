from aiogram import types


def get_keyboard():
    buttons = [
        types.InlineKeyboardButton(text='Получить котика', callback_data='get_cat'),
        types.InlineKeyboardButton(text='Сколько у нас котиков?', callback_data='how_many'),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def get_one_button():
    buttons = [
        types.InlineKeyboardButton(text='Получить котика', callback_data='get_cat'),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard
