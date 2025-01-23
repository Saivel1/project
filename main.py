import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
BOT_TOKEN = '7558977298:AAFfnstvUPQl6ytks8GwGx-JlqAm9vryL9U'

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="Да", callback_data="yes")
    await message.answer("Нажмите кнопку 'Да'", reply_markup=builder.as_markup())

@dp.callback_query_handler(lambda c: c.data == "yes")
async def process_callback_yes(callback_query: types.CallbackQuery):
    await callback_query.answer("Вы нажали 'Да'", show_alert=True) # всплывающее уведомление
    await callback_query.message.answer("Вы выбрали 'Да'")
    # Важно отправить ответ на callback_query, чтобы убрать "часики" на кнопке
    await callback_query.answer()

async def main():
    await dp.start_polling(bot)

if name == "main":
    asyncio.run(main())
