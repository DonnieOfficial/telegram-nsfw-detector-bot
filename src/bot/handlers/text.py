from aiogram import Router, F
from aiogram.types import Message

from src.core.config import config
from src.services.nsfw_detector import NSFWDetector


router = Router()

@router.message(F.text)
async def text_handler(message: Message, nsfw_detector = NSFWDetector) -> None:
    if len(message.text) > config.MAX_TEXT_LENGTH:
        await message.answer(f"Text is too long. Maximum length: {config.MAX_TEXT_LENGTH} characters.")
        return

    try:
        result = await nsfw_detector.detect_text(message.text)

        if result["is_nsfw"]:
            details = "\n".join([f"{k}: {v:.2%}" for k, v in result["details"].items()])
            await message.answer(
                f"⚠️ NSFW content detected in text!\n\n"
                f"Probabilities:\n{details}\n\n"
                f"Total NSFW rating: {result['nsfw']:.2%}"
            )
        else:
            await message.answer(
                "✅ Text is safe\n"
                f"NSFW probability: {result['safe']:.2%}"
            )
    except Exception as error:
        await message.answer(f"Error processing text: {str(error)}")