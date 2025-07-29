import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import TOKEN
from handlers import router
from db import async_main # ИСПРАВЛЕНО: Импортируем переименованную функцию для инициализации БД


bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():

    # await async_main()

    dp.include_router(router)

    await dp.start_polling(bot)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:

        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен по команде пользователя (KeyboardInterrupt)!')
    except Exception as e:

        logging.error(f"Произошла непредвиденная ошибка: {e}")
    finally:

        print('Бот завершил работу.')