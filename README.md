# Telegram Financial Text Translator Bot

A Telegram bot that specializes in translating financial market texts from any language into Persian. The bot supports various media types and provides professional translations while maintaining appropriate financial terminology.

## Features

- 🔤 Text Translation

  - Translates any text message to Persian
  - Maintains financial terminology and professional language
  - Preserves original formatting and structure

- 📸 Media Support

  - Translates captions for photos, videos, and documents
  - Handles media groups (multiple photos/videos)
  - Supports voice messages and video notes with transcription

- 🎥 YouTube Integration

  - Extracts audio from YouTube videos
  - Transcribes and translates video content
  - Maintains context and formatting

- 🔒 Access Control
  - Channel support
  - Group support
  - Private chat support
  - Configurable allowed users/channels/groups

## Setup

1. Clone the repository

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables:

   - Copy `.env.example` to `.env`
   - Fill in the required values:
     - `TELEGRAM_BOT_API_TOKEN`: Your Telegram bot token from [@BotFather](https://t.me/BotFather)
     - `OPENAI_API_KEY`: Your OpenAI API key for translations
     - `ALLOWED_CHANNELS`: Comma-separated list of allowed channel IDs
     - `ALLOWED_USERS`: Comma-separated list of allowed user IDs
     - `ALLOWED_GROUPS`: Comma-separated list of allowed group IDs
     - `MODEL`: OpenAI model to use (default: gpt-4o-mini)
     - `PROMPT`: System prompt for translation style

4. Run the bot:

```bash
python bot.py
```

## Dependencies

Key dependencies include:

- python-telegram-bot: Telegram Bot API wrapper
- openai: OpenAI API integration
- moviepy: Video processing
- yt-dlp: YouTube video download
- python-dotenv: Environment variable management

For a complete list of dependencies, see `requirements.txt`.

## Usage

1. Start a private chat with the bot or add it to an allowed group/channel
2. Send any text message to translate it to Persian
3. Send media with captions to get translated captions
4. Send YouTube links to get video content translated
5. Send voice messages or video notes for transcription and translation

## Security

- The bot only responds to messages from authorized users, channels, and groups
- API keys and tokens are stored securely in environment variables
- Access control is enforced for all bot functions

## Error Handling

The bot includes comprehensive error handling for:

- Media processing failures
- Translation service issues
- Network connectivity problems
- Invalid message types
- Authorization failures

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
