import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook
from aiohttp import web

API_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_HOST = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", 5000))

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

CHANNEL_USERNAME = "@philphilosophy"
VIDEO_URL = "https://t.me/philphilosophy/13"

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    user = message.from_user
    chat_member = await bot.get_chat_member(CHANNEL_USERNAME, user.id)

    if chat_member.status in ["member", "creator", "administrator"]:
        await message.answer(
            f"Спасибо за подписку! Вот твой видеоурок и финансовая система:\n{VIDEO_URL}"
        )
    else:
        await message.answer(
            f"Перед получением материала, пожалуйста, подпишись на канал {CHANNEL_USERNAME}"
        )

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    await bot.delete_webhook()

def init_app():
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, webhook_handler)
    return app

async def webhook_handler(request):
    data = await request.json()
    update = types.Update.to_object(data)
    await dp.process_update(update)
    return web.Response()

if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
