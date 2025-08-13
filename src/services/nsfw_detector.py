from PIL import Image
from io import BytesIO
from transformers import pipeline
from typing import Dict


class NSFWDetector:
    def __init__(self, model_name: str = "Falconsai/nsfw_image_detection", threshold: float = 0.85):
        self.pipeline = pipeline("image-classification", model = model_name)
        self.threshold = threshold
        self.classes = {
            "safe": ["normal"],
            "nsfw": ["nsfw"],
        }

    async def detect(self, image_bytes: bytes) -> Dict[str, float]:
        try:
            image = Image.open(BytesIO(image_bytes)).convert("RGB")
            results = self.pipeline(image)

            probs = {result["label"]: result["score"] for result in results}

            return {
                "safe": sum(probs.get(c, 0) for c in self.classes["safe"]),
                "nsfw": sum(probs.get(c, 0) for c in self.classes["nsfw"]),
                "is_nsfw": sum(probs.get(c, 0) for c in self.classes["nsfw"]) > self.threshold,
                "details": probs,
            }
        except Exception as error:
            raise ValueError(f"Image processing error: {str(error)}")