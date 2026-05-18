import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode

from config import Config, load_config
from database import load_db, save_db
from handlers import user_commands_router, unknown_router, user_callbacks_router
from keyboards import set_main_menu
from services import prepare_book
from log_config import setup_logging


logger = logging.getLogger(__name__)

async def main() -> None:
    config: Config = load_config()

    setup_logging(
        level=config.log.level,
        log_file='bot.log',
        console_output=True,
    )

    logger.info('Starting bot')

    session = AiohttpSession(proxy=config.proxy.url) if config.proxy else None
    if session:
        logger.info(f"Proxy connected: {config.proxy.type}://{config.proxy.ip}:{config.proxy.port}")

    bot = Bot(
        token=config.bot.token,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    logger.info('Preparing book')
    book = prepare_book('book/clockwork_orange.txt')
    logger.info(f"The book is uploaded. Total pages: {len(book)}")

    logger.info('Loading database')
    db = await load_db()
    logger.info("Database loaded")

    dp.workflow_data.update(book=book, db=db)

    await set_main_menu(bot)

    dp.include_router(user_commands_router)
    dp.include_router(user_callbacks_router)
    dp.include_router(unknown_router)
    logger.info("Routers registered")

    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Webhook deleted")

    try:
        logger.info("Bot configured and starting")
        await dp.start_polling(bot)
    finally:
        logger.info("Saving database...")
        await save_db(db)
        logger.info("Database saved")

        if session:
            await session.close()
            logger.info("Session closed")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped by developer")
    except Exception as e:
        logging.error(f"Critical error: {e}", exc_info=True)