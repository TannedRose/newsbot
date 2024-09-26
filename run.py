from aiogram import Bot, Dispatcher, F
import asyncio
import logging

from sqlalchemy.exc import IntegrityError

from config import TOKEN, BLACK_LIST, ADMIN_ID
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
import keyboards as kb
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import requests as rq
from models import async_main

bot = Bot(token=TOKEN)
dp = Dispatcher()


class Getnews(StatesGroup):
    caption = State()
    photo = State()
    id = State()
    username = State()
    mention = State()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(text="Привет! это бот для предложения новостей")
    await message.answer(text="‼️Советуем прочитать правила подачи новостей‼️", reply_markup=kb.main)
    try:
        await rq.add_user(user_id=message.from_user.id, name=message.from_user.first_name,
                      username=message.from_user.username)
    except IntegrityError:
        await rq.add_user(user_id=message.from_user.id, name=message.from_user.first_name, username="None")


@dp.message(F.text == "Правила подачи новостей")
async def news1(message: Message):
    global pin
    await message.answer(text='1. Мы не принимаем новости, содержащие: личностные оскробления, 18+, '
                                    'издевательские посты.\n\n2. Принимаем: все, кроме выше упомянутых, поздравления с '
                                    'днем рождения и тд.\n\n3. К вашим новостям должна быть прекреплена минимум 1 '
                                    'фотография, сделанная вами или вашими друзьями.\n\n4. Вы можете описать саму '
                                    'новость в любом формате, так как в будущем она попадет админам, после чего её '
                                    'оформят и выставят в канал.\n\nP.S.\nчтобы отправить новость нажмите на кнопку '
                                    '"Подать новость" и следуйте указаниям бота')


@dp.message(F.text == "Подать новость")
async def news1(message: Message, state: FSMContext):
    await message.answer(text="Введите описание произошедшего", reply_markup=kb.main_meny)
    await state.set_state(Getnews.caption)


@dp.message(F.text == "Вернуться в глaвное мeню")
async def news1(message: Message, state: FSMContext):
    await message.answer(text="Вы вернулись в главное меню", reply_markup=kb.main)
    await state.clear()


@dp.message(Getnews.caption)
async def news2(message: Message, state: FSMContext):
    await state.update_data(id=message.from_user.id, username=message.from_user.username)
    if message.photo:
        len_caption = message.caption
        if len(message.caption) > 1024:
            await message.answer(text=f"Слишком длииная новость😶 максимальная длина 1024 символа (вы ввели "
                                      f"{len_caption}, введите новость в более краткой форме или "
                                      f"выйдите в главное меню)", reply_markup=kb.main_meny)
        else:
            await state.update_data(caption=message.caption)
            await state.update_data(photo=message.photo[-1].file_id)
            await message.answer("хотите чтобы вас отметили в новости?", reply_markup=kb.last)

    elif message.text:
        len_text = message.text
        if len(message.text) > 1024:
            await message.answer(text=f"Слишком длииная новость😶 максимальная длина 1024 символа (вы ввели "
                                      f"{len_text}, введите новость в более краткой форме или "
                                      f"выйдите в главное меню)", reply_markup=kb.main_meny)
        else:
            await state.update_data(caption=message.text)
            await state.set_state(Getnews.photo)
            await message.answer("отправьте фото с места событий", reply_markup=kb.main_meny)


@dp.message(Getnews.photo)
async def news3(message: Message, state: FSMContext):
    if message.photo:
        await state.update_data(photo=message.photo[-1].file_id)
        await message.answer("хотите чтобы вас отметили в новости?", reply_markup=kb.last)

    else:
        await message.answer(text="Отправте именно фото!")


@dp.callback_query(F.data == "yes")
async def yes(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await state.update_data(mention="да")
    data_news = await state.get_data()
    await bot.send_photo(chat_id=ADMIN_ID, photo=data_news['photo'], caption=f"вопрос: {data_news['caption']}"
                                                                             f"\nid пользователя: {data_news['id']}"
                                                                             f"\nusername: {data_news['username']}"
                                                                             f"\nотметить под постом: {data_news['mention']}")
    await callback.message.answer(text="новость успешно отправлена на рассмотрение администратору",
                                  reply_markup=kb.main)
    await bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                        reply_markup=None)
    await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                text='хотите чтобы вас отметили в новости?\n\n (вы выбрали "да")')
    await state.clear()


@dp.callback_query(F.data == "no")
async def yes(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await state.update_data(mention="нет")
    data_news = await state.get_data()
    await bot.send_photo(chat_id=ADMIN_ID, photo=data_news['photo'], caption=f"вопрос: {data_news['caption']}"
                                                                             f"\nid пользователя: {data_news['id']}"
                                                                             f"\nusername: {data_news['username']}"
                                                                             f"\nотметить под постом: {data_news['mention']}")
    await callback.message.answer(text="новость успешно отправлена на рассмотрение администратору",
                                  reply_markup=kb.main)
    await bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                        reply_markup=None)
    await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                text='хотите чтобы вас отметили в новости?\n\n (вы выбрали "нет")')
    await state.clear()


# @dp.callback_query(F.data == "pin")
# async def nex(callback: CallbackQuery):
#     global pin
#     print(pin)
#     await callback.answer('')
#     await bot.pin_chat_message(chat_id=callback.message.from_user.id, message_id=pin)
#     await callback.message.answer("сообщение закреплено", reply_markup=kb.main)


async def main():
    await async_main()
    # dp.include_router(router=router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("выход")
