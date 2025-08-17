# NSFW Content Detection Telegram Bot
A smart Telegram bot designed to detect Not Safe For Work (NSFW) content in various message formats including text, images, stickers, emojis, and videos. The bot uses advanced machine learning models to analyze content and provide probability scores for different NSFW categories.

**Features:**
- **Multi-format Support: Detects NSFW content in:**
    - Text messages;
    - Images;
    - Stickers (including animated);
    - Emojis;
    - Videos (frame-by-frame analysis).
- **Detailed Analysis:**
    - Provides probability scores for different NSFW categories;
    - For videos: analyzes multiple frames and provides average/max NSFW probabilities;
    - For stickers: combines analysis of both visual content and associated emoji/text.
- **Configurable Thresholds:**
    - Adjustable sensitivity for NSFW detection;
    - Customizable file size limits.
- **Performance Optimized:**
    - Asynchronous processing;
    - Video frame extraction in background threads;
    - Efficient memory handling for large files.

## Technologies Used
- **Programming Language**: Python.
- **IDE**: Visual Studio Code.
- **AI Framework**: HuggingFace Transformers.
- **Computer Vision**: OpenCV, PIL.
- **Telegram Integration**: Aiogram.
- **Async Processing**: Asyncio, ThreadPoolExecutor.
- **Configuration**: Pydantic settings.
- **Logging**: Custom logging system with file rotation.

## Installation
**1. Clone the repository:**
```sh
git clone https://github.com/DonnieOfficial/telegram-nsfw-detector-bot.git
```
**2. Set up environment:**
* Rename `.env.example` to `.env`;
* Add your Telegram bot token `BOT_TOKEN=your_actual_bot_token_here`.

**3. Install dependencies:**
```sh
poetry install
```

**4. Run the bot:**
```sh
poetry run python -m src.main
```

## Usage
* Start a chat with your bot in Telegram.
* Send any of the following to analyze:
    - Text messages;
    - Images;
    - Stickers;
    - Videos (up to 10MB).
* The bot will respond with:
    - ✅ Safe content confirmation with probability score;
    - ⚠️ NSFW content warning with detailed probabilities.
* Example commands:
    - `/start` - Get welcome message;
    - Send any photo - Get NSFW analysis;
    - Send text - Get text sentiment analysis.

## Configuration
Customize the bot behavior by modifying these values in `src/core/config.py`:
* `MAX_FILE_SIZE`: Maximum file size for uploads (default: 10MB);
* `MAX_TEXT_LENGTH`: Maximum text length for analysis (default: 2000 chars);
* `MAX_VIDEO_DURATION`: Maximum video duration to process (default: 60s).

Or adjust the detection threshold in `NSFWDetector` initialization.

## Contribution
* If you would like to contribute to the project, please fork the repository and submit a pull request. We welcome all improvements and additions.

## License
* This project is licensed under the MIT License. See the `LICENSE` file for details.

## Documentation
* [Aiogram](https://aiogram.dev).
* [Pydantic](https://docs.pydantic.dev).
* [OpenCV](https://docs.opencv.org/4.x).
* [Pillow](https://pillow.readthedocs.io/en/stable).
* [Asyncio](https://docs.python.org/3/library/asyncio.html).
* [HuggingFace Transformers](https://huggingface.co).

## Authors

- [@DonnieOfficial](https://github.com/DonnieOfficial)
