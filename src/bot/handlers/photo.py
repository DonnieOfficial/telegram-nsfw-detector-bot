from aiogram import Router, F
from aiogram.types import Message, PhotoSize

from src.core.config import config
from src.services.nsfw_detector import NSFWDetector


router = Router()

@router.message(F.photo)
async def photo_handler(message: Message, nsfw_detector = NSFWDetector) -> None:
    photo: PhotoSize = max(message.photo, key = lambda p: p.file_size)

    if photo.file_size > config.MAX_FILE_SIZE:
        await message.answer("The image is too big. Maximum size: 10MB.")
        return

    file = await message.bot.get_file(photo.file_id)
    file_bytes = await message.bot.download_file(file.file_path)

    result = await nsfw_detector.detect_image(image_bytes = file_bytes.read())

    if result["is_nsfw"]:
        details = "\n".join([f"{k}: {v:.2%}" for k, v in result["details"].items()])
        await message.answer(
            f"⚠️ NSFW content detected!\n\n"
            f"Probabilities:\n{details}\n\n"
            f"Total NSFW rating: {result['nsfw']:.2%}"
        )
    else:
        await message.answer(
            "✅ Image is safe\n"
            f"NSFW probability: {result['nsfw']:.2%}"
        )