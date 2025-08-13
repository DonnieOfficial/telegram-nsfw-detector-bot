from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart


router = Router()

@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(text = "Hi! Send me a photo to analyze for NSFW content.")