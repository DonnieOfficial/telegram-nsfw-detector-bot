from aiogram import Router, F
from aiogram.types import Message, Video

from src.core.config import config
from src.services.nsfw_detector import NSFWDetector
from src.services.video_processor import extract_frames, analyze_video_frames


router = Router()

@router.message(F.video)
async def video_handler(message: Message, nsfw_detector: NSFWDetector) -> None:
    video: Video = message.video

    if video.file_size > config.MAX_FILE_SIZE:
        await message.answer("The video is too big. Maximum size: 10MB.")
        return

    try:
        file = await message.bot.get_file(video.file_id)
        video_bytes = await message.bot.download_file(file.file_path)

        await message.answer("⏳ Processing video...")
        frames = await extract_frames(video_bytes.read())

        if not frames:
            await message.answer("❌ Could not extract frames from video")
            return

        result = await analyze_video_frames(frames, nsfw_detector)

        if result["is_nsfw"]:
            details = (
                f"Average NSFW: {result['nsfw']:.2%}\n"
                f"Max frame NSFW: {result['details']['max_nsfw']:.2%}\n"
                f"NSFW frames: {result['details']['nsfw_frames']}/{result['details']['total_frames']}"
            )
            await message.answer(
                f"⚠️ NSFW content detected in video!\n\n"
                f"Video analysis results:\n{details}\n\n"
                f"Total NSFW rating: {result['nsfw']:.2%}"
            )
        else:
            await message.answer(
                "✅ Video is safe\n"
                f"Average NSFW probability: {result['nsfw']:.2%}\n"
                f"Analyzed frames: {result['details']['total_frames']}"
            )
    except Exception as error:
        await message.answer(f"Error processing video: {str(error)}")