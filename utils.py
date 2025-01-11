from io import BytesIO
import os
import yt_dlp
from openai import OpenAI, AsyncOpenAI
import settings


client = AsyncOpenAI(
    api_key=settings.OPENAI_API_KEY,
)


async def download_youtube_audio(url: str) -> BytesIO:
    """
    Downloads audio from a YouTube video and returns it as BytesIO object.
    """
    try:
        if not os.path.exists("./tempfiles"):
            os.makedirs("./tempfiles")

        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "outtmpl": "./tempfiles/%(id)s.%(ext)s",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_id = info["id"]
            audio_path = f"./tempfiles/{video_id}.mp3"

            # Read the audio file into BytesIO
            with open(audio_path, "rb") as f:
                audio_bytes = BytesIO(f.read())
                audio_bytes.name = f"{video_id}.mp3"

            # Clean up the temporary file
            os.remove(audio_path)

            return audio_bytes
    except Exception as e:
        print(f"Error downloading YouTube audio: {e}")
        raise


async def translate_text(text: str) -> str:
    """
    Translates the given text to Persian using OpenAI's Chat Completion API.
    """
    try:
        response = await client.chat.completions.create(
            model=settings.MODEL,
            messages=[
                {
                    "role": "system",
                    "content": settings.PROMPT,
                },
                {
                    "role": "user",
                    "content": f"متن رو به صورت تخصصی در حوضه بازار مالی ترجمه و مرتب کن: \n\n{text}",
                },
            ],
            temperature=0.3,
        )
        translated_text = response.choices[0].message.content.strip()
        return translated_text
    except Exception as e:
        print(f"Error during translation: {e}")
        return "مشکلی در ترجمه متن پیش آمد!"


async def transcribe_audio(audio_file: BytesIO) -> str:
    try:
        transcription = await client.audio.transcriptions.create(
            model="whisper-1", file=audio_file
        )
        return transcription.text
    except Exception as e:
        print(e)
        return "Failed to transcribe the audio."


def split_message(message, max_length=4096):
    """
    Splits the message into chunks not exceeding max_length characters.
    Attempts to split at newline characters or spaces for better readability.
    """
    if len(message) <= max_length:
        return [message]

    chunks = []
    current_chunk = ""

    for line in message.split("\n"):
        if len(current_chunk) + len(line) + 1 > max_length:
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""
        if len(line) + 1 > max_length:
            # Split the line into smaller parts
            for i in range(0, len(line), max_length):
                chunks.append(line[i : i + max_length])
        else:
            current_chunk += line + "\n"

    if current_chunk:
        chunks.append(current_chunk)

    return chunks
