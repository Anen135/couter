import asyncio
from aiogram import Bot
from router import TOKEN, dp

# Run the bot
async def main() -> None:
    bot = Bot(token=TOKEN)
    print("start polling")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())