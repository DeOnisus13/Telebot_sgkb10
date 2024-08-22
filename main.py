import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from dotenv import load_dotenv


class BookingStates(StatesGroup):
    """Класс для определения состояния"""

    waiting_for_info = State()


async def main():
    load_dotenv(".env")

    API_TOKEN = os.getenv("API_TOKEN")
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Хэндлер для команды /start
    @dp.message(Command(commands=["start"]))
    async def send_welcome(message: types.Message, state: FSMContext):
        await state.clear()  # Очищаем состояние на случай, если пользователь начинает заново
        await message.reply(
            "Здравствуйте. Вас приветствует чат-бот ГУЗ 'Саратовская городская клиническая больница №10'. "
            "С моей помощью вы можете записаться на прием к врачу, вызвать врача на дом или отменить запись."
        )

        keyboard = ReplyKeyboardBuilder()
        keyboard.add(types.KeyboardButton(text="Запись к врачу"))
        keyboard.add(types.KeyboardButton(text="Вызов на дом"))
        keyboard.add(types.KeyboardButton(text="Отмена записи"))
        keyboard.adjust(1)  # Выставляем количество кнопок в ряду

        await message.answer(
            "Выберите что вас интересует?",
            reply_markup=keyboard.as_markup(resize_keyboard=True),
        )

    # Хэндлер для "Записи к врачу"
    @dp.message(F.text == "Запись к врачу")
    async def zapis(message: types.Message, state: FSMContext):
        await message.reply(
            "Введите ваше ФИО, телефон для связи, адрес и врача, к которому хотите записаться.",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        await state.set_state(BookingStates.waiting_for_info)
        await state.update_data(action="Запись к врачу")

    # Хэндлер для "Вызова на дом"
    @dp.message(F.text == "Вызов на дом")
    async def vizov(message: types.Message, state: FSMContext):
        await message.reply(
            "Введите ваше ФИО, телефон для связи, адрес и причину вызова врача.",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        await state.set_state(BookingStates.waiting_for_info)
        await state.update_data(action="Вызов на дом")

    # Хэндлер для "Отмены записи"
    @dp.message(F.text == "Отмена записи")
    async def otmena(message: types.Message, state: FSMContext):
        await message.reply(
            "Введите ваше ФИО, телефон для связи, адрес, а также к какому врачу и на какое время вы были записаны.",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        await state.set_state(BookingStates.waiting_for_info)
        await state.update_data(action="Отмена записи")

    # Хэндлер для сбора данных
    @dp.message(StateFilter(BookingStates.waiting_for_info))
    async def process_info(message: types.Message, state: FSMContext):
        group_to_send_message = os.getenv("GROUP")
        user_data = await state.get_data()
        action = user_data.get("action")
        user_id = message.from_user.id
        user_name = message.from_user.username
        text = f"{action}\nПользователь - [{user_name}](tg://user?id={str(user_id)})\n{message.text}"
        await bot.send_message(
            chat_id=group_to_send_message, text=text, parse_mode="Markdown"
        )
        await message.reply("Спасибо. В ближайшее время с вами свяжется сотрудник ЛПУ.")
        await message.reply("Если вы хотите перезапустить чат, нажмите /start")
        await state.clear()  # Очищаем состояние после завершения диалога

    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
