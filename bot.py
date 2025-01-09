# bot.py

import os
import logging
import asyncio
from io import BytesIO
from moviepy.video.io.VideoFileClip import VideoFileClip

from telegram import (
    Update,
    InputMediaPhoto,
    InputMediaVideo,
    InputMediaAudio,
    InputMediaDocument,
)
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
)
from utils import translate_text, transcribe_audio, split_message
import settings

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Dictionary to keep track of media groups
media_groups = {}
MEDIA_GROUP_TIMEOUT = (
    settings.MEDIA_GROUP_TIMEOUT
)  # seconds to wait before processing media group


# bot.py


async def send_long_message(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    text: str,
    reply_to_message_id: int = None,
):
    """
    Sends a long message by splitting it into chunks if necessary.

    :param context: The context from the handler.
    :param chat_id: The ID of the chat to send the message to.
    :param text: The message text to send.
    :param reply_to_message_id: (Optional) The message ID to reply to.
    """
    chunks = split_message(text, max_length=4096)

    for chunk in chunks:
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=chunk,
                reply_to_message_id=reply_to_message_id,
                parse_mode="HTML",  # Adjust as needed
            )
            # Optional: Add a short delay to respect rate limits
            await asyncio.sleep(0.1)
        except Exception as e:
            logger.error(f"Failed to send message chunk: {e}")
            # Optionally, implement retry logic here


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles incoming messages: text, media, and media groups.
    """
    try:
        message = update.effective_message
        chat_id = message.chat.id

        # Check if the message is part of a media group
        if message.media_group_id:
            media_group_id = message.media_group_id

            if media_group_id not in media_groups:
                # Initialize a new media group entry with a timeout
                media_groups[media_group_id] = {"messages": [], "chat_id": chat_id}
                # Schedule processing after a delay
                asyncio.create_task(process_media_group(media_group_id, context))

            # Append the current message to the media group
            media_groups[media_group_id]["messages"].append(message)

        else:
            # Handle single media messages or text
            await handle_single_message(message, context)

    except Exception as e:
        logger.error(f"Error handling message: {e}")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="An error occurred while processing your message.",
            reply_to_message_id=update.effective_message.message_id,
        )


async def process_media_group(media_group_id: str, context: ContextTypes.DEFAULT_TYPE):
    """
    Waits for a timeout and then processes the media group by translating captions and resending.
    """
    await asyncio.sleep(MEDIA_GROUP_TIMEOUT)  # Wait for more messages in the group

    group = media_groups.pop(media_group_id, {})
    messages = group.get("messages", [])
    chat_id = group.get("chat_id")

    if not messages:
        logger.warning(f"No messages found for media group {media_group_id}.")
        return

    media = []
    reply_to_message_id = messages[
        0
    ].message_id  # Reply to the first message in the group

    for msg in messages:
        media_item = None
        translated_caption = ""

        # Determine the media type and prepare InputMedia objects
        if msg.photo:
            # For photos, choose the highest resolution
            photo = msg.photo[-1]
            # Translate caption if exists
            if msg.caption:
                # translated_caption = await translate_text(msg.caption)
                translated_caption = "ترجمه شد!"
            media_item = InputMediaPhoto(
                media=photo.file_id,
                caption=translated_caption if translated_caption else None,
            )
        elif msg.video:
            video = msg.video
            if msg.caption:
                # translated_caption = await translate_text(msg.caption)
                translated_caption = "ترجمه شد!"
            media_item = InputMediaVideo(
                media=video.file_id,
                caption=translated_caption if translated_caption else None,
            )
        elif msg.audio:
            audio = msg.audio
            if msg.caption:
                # translated_caption = await translate_text(msg.caption)
                translated_caption = "اهنگ ترجمه شد!"
            media_item = InputMediaAudio(
                media=audio.file_id,
                caption=translated_caption if translated_caption else None,
            )
        elif msg.document:
            document = msg.document
            if msg.caption:
                # translated_caption = await translate_text(msg.caption)
                translated_caption = "ترجمه شد!"
            media_item = InputMediaDocument(
                media=document.file_id,
                caption=translated_caption if translated_caption else None,
            )
        elif msg.voice:

            voice = msg.voice
            transcription = "متن"

            await context.bot.send_message(
                chat_id=chat_id, text=transcription, reply_to_message_id=msg.message_id
            )
        else:
            # Unsupported media type; skip
            logger.warning(f"Unsupported media type in message {msg.message_id}.")
            continue

        if media_item:
            media.append(media_item)

    if media:
        try:
            await context.bot.send_media_group(
                chat_id=chat_id, media=media, reply_to_message_id=reply_to_message_id
            )
            logger.info(
                f"Sent translated media group with {len(media)} items to chat {chat_id}."
            )
        except Exception as e:
            logger.error(f"Failed to send media group: {e}")
            await context.bot.send_message(
                chat_id=chat_id,
                text="Failed to send the translated media group.",
                reply_to_message_id=reply_to_message_id,
            )


async def handle_single_message(message, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles single text or media messages.
    """
    chat_id = message.chat.id
    if any(
        [
            message.photo,
            message.video,
            message.audio,
            message.document,
            message.voice,
            message.video_note,
        ]
    ):
        translated_caption = ""

        if message.photo:
            photo = message.photo[-1]
            if message.caption:
                translated_caption = await translate_text(message.caption)
            try:
                await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=photo.file_id,
                    caption=translated_caption if translated_caption else None,
                    reply_to_message_id=message.message_id,
                )
                logger.info(f"Sent translated photo to chat {chat_id}.")
            except Exception as e:
                logger.error(f"Failed to send photo: {e}")
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="Failed to send the translated photo.",
                    reply_to_message_id=message.message_id,
                )
        elif message.video:
            video = message.video
            if message.caption:
                # translated_caption = await translate_text(message.caption)
                translated_caption = "ترجمه شد!"

            try:
                await context.bot.send_video(
                    chat_id=chat_id,
                    video=video.file_id,
                    caption=translated_caption if translated_caption else None,
                    reply_to_message_id=message.message_id,
                )
                logger.info(f"Sent translated video to chat {chat_id}.")
            except Exception as e:
                logger.error(f"Failed to send video: {e}")
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="Failed to send the translated video.",
                    reply_to_message_id=message.message_id,
                )
        elif message.audio:
            audio = message.audio
            file_id = audio.file_id
            new_file = await context.bot.get_file(file_id)

            file_bytes = await new_file.download_as_bytearray()
            audio_bytes = BytesIO(file_bytes)
            audio_bytes.name = "audio.mp3"

            transcription = await transcribe_audio(audio_bytes)
            translated_caption = await translate_text(transcription)

            try:
                await send_long_message(
                    context=context,
                    chat_id=chat_id,
                    text=translated_caption if translated_caption else None,
                    reply_to_message_id=message.message_id,
                )
                logger.info(f"Sent translated audio to chat {chat_id}.")
            except Exception as e:
                logger.error(f"Failed to send audio: {e}")
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="Failed to send the translated audio.",
                    reply_to_message_id=message.message_id,
                )
        elif message.document:
            document = message.document
            if message.caption:
                translated_caption = await translate_text(message.caption)
            try:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=translated_caption if translated_caption else None,
                    reply_to_message_id=message.message_id,
                )
                logger.info(f"Sent translated document to chat {chat_id}.")
            except Exception as e:
                logger.error(f"Failed to send document: {e}")
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="Failed to send the translated document.",
                    reply_to_message_id=message.message_id,
                )

        elif message.voice:
            voice = message.voice
            file_id = voice.file_id
            new_file = await context.bot.get_file(file_id)

            file_bytes = await new_file.download_as_bytearray()
            audio_bytes = BytesIO(file_bytes)
            audio_bytes.name = "voice_message.ogg"

            transcription = await transcribe_audio(audio_bytes)
            translated_caption = await translate_text(transcription)

            try:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=translated_caption if translated_caption else None,
                    reply_to_message_id=message.message_id,
                )
                logger.info(f"Sent translated audio to chat {chat_id}.")
            except Exception as e:
                logger.error(f"Failed to send audio: {e}")
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="Failed to send the translated audio.",
                    reply_to_message_id=message.message_id,
                )
        elif message.video_note:
            video_note = message.video_note
            file_id = video_note.file_id
            new_file = await context.bot.get_file(file_id)
            if not os.path.exists("./tempfiles"):
                os.makedirs("./tempfiles")
            path = f"./tempfiles/{file_id}.mp4"

            if not os.path.exists(path):
                await new_file.download_to_drive(custom_path=path)
            mp4_file = path
            mp3_file = f"./tempfiles/{file_id}.mp3"
            video_clip = VideoFileClip(mp4_file)
            audio_clip = video_clip.audio
            if not os.path.exists(mp3_file):
                audio_clip.write_audiofile(mp3_file)

            audio_clip.close()
            video_clip.close()

            with open(mp3_file, "rb") as f:
                audio_bytes = BytesIO(f.read())
                audio_bytes.name = f"{file_id}.mp3"
                transcription = await transcribe_audio(audio_bytes)
                translated_caption = await translate_text(transcription)
            try:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=translated_caption if translated_caption else None,
                    reply_to_message_id=message.message_id,
                )

                logger.info(f"Sent translated audio to chat {chat_id}.")
            except Exception as e:
                logger.error(f"Failed to send audio: {e}")
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="Failed to send the translated audio.",
                    reply_to_message_id=message.message_id,
                )
            finally:
                for file_path in [mp4_file, mp3_file]:
                    try:
                        if os.path.exists(file_path):
                            os.remove(file_path)
                            logger.info(f"Removed temporary file: {file_path}")
                    except Exception as remove_error:
                        logger.error(f"Error removing file {file_path}: {remove_error}")

    elif message.text:
        original_text = message.text
        try:
            translated_text = await translate_text(original_text)
            if translated_text:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=translated_text,
                    reply_to_message_id=message.message_id,
                )
                logger.info(f"Sent translated text to chat {chat_id}.")
        except Exception as e:
            logger.error(f"Failed to translate/send text: {e}")
            await context.bot.send_message(
                chat_id=chat_id,
                text="Failed to translate your message.",
                reply_to_message_id=message.message_id,
            )
    else:
        # Unsupported message type
        logger.warning(f"Received unsupported message type in chat {chat_id}.")
        await context.bot.send_message(
            chat_id=chat_id,
            text="Unsupported message type. Please send text or media with captions.",
            reply_to_message_id=message.message_id,
        )


def main():
    """
    Initializes and runs the Telegram bot.
    """
    # Create the Application and pass it your bot's token
    application = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

    # Add a handler for all message types
    message_handler = MessageHandler(filters.ALL, handle_message)
    application.add_handler(message_handler)

    # Start the Bot
    logger.info("Bot is running...")
    application.run_polling()


if __name__ == "__main__":
    main()
