import openai
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message

openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

ALLOWED_USERS = []  # можешь позже добавить user_id друзей

@dp.message_handler()
async def gpt_response(message: Message):
    if ALLOWED_USERS and message.from_user.id not in ALLOWED_USERS:
        await message.reply("⛔ Доступ закрыт.")
        return

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # можно "gpt-3.5-turbo"
            messages=[{"role": "user", "content": message.text}],
            temperature=0.7,
            max_tokens=1000
        )
        await message.reply(response.choices[0].message.content.strip())
    except Exception as e:
        await message.reply(f"Ошибка: {e}")

async def main():
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())

