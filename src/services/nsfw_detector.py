from PIL import Image
from io import BytesIO
from transformers import pipeline
from typing import Dict


class NSFWDetector:
    def __init__(
        self,
        image_model_name: str = "Falconsai/nsfw_image_detection",
        text_model_name: str = "blanchefort/rubert-base-cased-sentiment-rusentiment",
        threshold: float = 0.85
    ):
        self.image_pipeline = pipeline("image-classification", model = image_model_name)
        self.text_pipeline = pipeline("text-classification", model = text_model_name)
        self.threshold = threshold
        self.image_classes = {
            "safe": ["normal"],
            "nsfw": ["nsfw"],
        }
        self.text_classes = {
            "safe": ["positive", "neutral"],
            "nsfw": ["negative"],
        }

    async def detect_image(self, image_bytes: bytes) -> Dict[str, float]:
        try:
            image = Image.open(BytesIO(image_bytes)).convert("RGB")
            results = self.image_pipeline(image)

            probs = {result["label"]: result["score"] for result in results}

            return {
                "safe": sum(probs.get(c, 0) for c in self.image_classes["safe"]),
                "nsfw": sum(probs.get(c, 0) for c in self.image_classes["nsfw"]),
                "is_nsfw": sum(probs.get(c, 0) for c in self.image_classes["nsfw"]) > self.threshold,
                "details": probs,
            }
        except Exception as error:
            raise ValueError(f"Image processing error: {str(error)}")

    async def detect_text(self, text: str) -> Dict[str, float]:
        try:
            results = self.text_pipeline([text])[0]

            if isinstance(results, dict):
                results = [results]

            probs = {result["label"].lower(): result["score"] for result in results}

            return {
                "safe": sum(probs.get(c, 0) for c in self.text_classes["safe"]),
                "nsfw": sum(probs.get(c, 0) for c in self.text_classes["nsfw"]),
                "is_nsfw": sum(probs.get(c, 0) for c in self.text_classes["nsfw"]) > self.threshold,
                "details": probs,
            }
        except Exception as error:
            raise ValueError(f"Text processing error: {error}")