from aiogram import Router, F
from aiogram.types import Message, Sticker
from io import BytesIO
from PIL import Image

from src.services.nsfw_detector import NSFWDetector


router = Router()

@router.message(F.sticker)
async def sticker_handler(message: Message, nsfw_detector: NSFWDetector) -> None:
    sticker: Sticker = message.sticker

    try:
        text_to_analyze = ""
        if sticker.emoji:
            text_to_analyze += sticker.emoji + " "
        if sticker.set_name:
            text_to_analyze += sticker.set_name

        text_result = None
        if text_to_analyze:
            text_result = await nsfw_detector.detect_text(text_to_analyze)

        image_result = None
        file = await message.bot.get_file(sticker.file_id)
        file_bytes = await message.bot.download_file(file.file_path)

        with Image.open(BytesIO(file_bytes.read())) as img:
            with BytesIO() as buffer:
                img.convert("RGB").save(buffer, format = "JPEG")
                image_result = await nsfw_detector.detect_image(buffer.getvalue())

        combined_nsfw = max(
            text_result["nsfw"] if text_result else 0,
            image_result["nsfw"] if image_result else 0,
        )

        is_nsfw = combined_nsfw > nsfw_detector.threshold

        if is_nsfw:
            details = []
            if text_result:
                details.append(
                    f"Text analysis (from emoji/set):\n"
                    f"NSFW: {text_result['nsfw']:.2%}\n"
                    f"Details: {', '.join(f'{k}: {v:.2%}' for k, v in text_result['details'].items())}"
                )
            if image_result:
                details.append(
                    f"Image analysis:\n"
                    f"NSFW: {image_result['nsfw']:.2%}\n"
                    f"Details: {', '.join(f'{k}: {v:.2%}' for k, v in image_result['details'].items())}"
                )

            await message.answer(
                "⚠️ NSFW content detected in sticker!\n\n"
                + "\n\n".join(details) + "\n\n"
                f"Combined NSFW rating: {combined_nsfw:.2%}"
            )
        else:
            safe_details = []
            if text_result:
                safe_details.append(f"Text NSFW: {text_result['nsfw']:.2%}")
            if image_result:
                safe_details.append(f"Image NSFW: {image_result['nsfw']:.2%}")

            await message.answer(
                "✅ Sticker is safe\n"
                f"{' | '.join(safe_details)}"
            )
    except Exception as error:
        await message.answer(f"Error processing sticker: {str(error)}")