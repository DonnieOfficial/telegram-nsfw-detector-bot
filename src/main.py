import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.core.config import config
from src.core.logger import logger
from src.bot.handlers import setup_routers
from src.services.nsfw_detector import NSFWDetector


async def main():
    logger.info("Starting bot...")

    try:
        bot = Bot(
            token = config.BOT_TOKEN.get_secret_value(),
            default = DefaultBotProperties(parse_mode = ParseMode.HTML),
        )
        dp = Dispatcher()

        nsfw_detector = NSFWDetector()

        dp.include_router(setup_routers())
        dp.workflow_data.update(
            nsfw_detector = nsfw_detector,
            logger = logger,
        )

        await bot.delete_webhook(drop_pending_updates = True)

        logger.info("Bot started successfully")
        await dp.start_polling(bot)
    except Exception as error:
        logger.critical(f"Bot failed to start: {error}", exc_info = True)
    finally:
        await bot.session.close()
        logger.info("Bot stopped")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")