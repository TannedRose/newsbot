from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardRemove


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Правила подачи новостей")],
    [KeyboardButton(text="Подать новость")]
],
    resize_keyboard=True,
    input_field_placeholder="Воспользуйтесь кнопками",)

main_meny = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Вернуться в глaвное мeню")]
],
    resize_keyboard=True,)

last = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="да", callback_data="yes")],
    [InlineKeyboardButton(text="нет", callback_data="no")]
])

pin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="закрепить это сообщение", callback_data="pin")]
])

remove = ReplyKeyboardRemove()