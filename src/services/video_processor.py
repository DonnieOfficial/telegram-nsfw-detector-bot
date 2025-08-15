import cv2
import asyncio
import tempfile
import os

from io import BytesIO
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
from typing import Dict

from src.services.nsfw_detector import NSFWDetector


executor = ThreadPoolExecutor(max_workers = 2)

async def extract_frames(video_bytes: bytes, frame_interval: int = 10) -> list:
    def _extract():
        frames = []

        with tempfile.NamedTemporaryFile(suffix = ".mp4", delete = False) as temp_file:
            temp_file.write(video_bytes)
            temp_path = temp_file.name

        try:
            cap = cv2.VideoCapture(temp_path)

            frame_count = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                if frame_count % frame_interval == 0:
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frames.append(rgb_frame)

                frame_count += 1

            cap.release()
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

        return frames

    loop = asyncio.get_event_loop()
    frames = await loop.run_in_executor(executor, _extract)
    return frames

async def analyze_video_frames(frames: list, nsfw_detector: NSFWDetector) -> Dict:
    total_safe = 0.0
    total_nsfw = 0.0
    frame_results = []

    for frame in frames:
        pil_img = Image.fromarray(frame)
        with BytesIO() as buffer:
            pil_img.save(buffer, format = "JPEG")
            result = await nsfw_detector.detect_image(buffer.getvalue())

            total_safe += result["safe"]
            total_nsfw += result["nsfw"]
            frame_results.append(result)

    frame_count = len(frame_results)
    if frame_count == 0:
        return {
            "safe": 0.0,
            "nsfw": 0.0,
            "is_nsfw": False,
            "details": {"no_frames": 1.0},
        }

    avg_safe = total_safe / frame_count
    avg_nsfw = total_nsfw / frame_count

    details = {
        "avg_safe": avg_safe,
        "avg_nsfw": avg_nsfw,
        "max_nsfw": max(r["nsfw"] for r in frame_results),
        "nsfw_frames": sum(1 for r in frame_results if r["is_nsfw"]),
        "total_frames": frame_count,
    }

    return {
        "safe": avg_safe,
        "nsfw": avg_nsfw,
        "is_nsfw": avg_nsfw > nsfw_detector.threshold,
        "details": details,
    }