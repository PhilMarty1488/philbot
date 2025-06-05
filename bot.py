import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command

API_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@philphilosophy"
VIDEO_POST_LINK = "https://t.me/philphilosophy/13"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
    if member.status in ["member", "administrator", "creator"]:
        await message.answer(
            f"Спасибо за подписку! Вот твой видеоурок и финансовая система:
{VIDEO_POST_LINK}"
        )
    else:
        await message.answer(
            f"Чтобы получить доступ к материалам, подпишись на канал {CHANNEL_USERNAME} и нажми /start ещё раз."
        )

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
