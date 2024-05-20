import asyncio
from aiogram import Dispatcher
from aiogram.types.bot_command import BotCommand
import utils
from user_handler import router as user_router
from db import database

dp = Dispatcher()




async def main() -> None:
    bot = utils.get_bot()
    await bot.set_my_commands(commands=\
              [BotCommand(command='start',description='Начать'),
               BotCommand(command='styles',description='Жанры'),
               BotCommand(command='books', description='Книги'),
               BotCommand(command='authors', description='Авторы')])
    # routers here
    dp.include_router(user_router)
    await database.connect()
    #
    await dp.start_polling(bot)
    await database.disconnect()




if __name__ == "__main__":
    asyncio.run(main())
