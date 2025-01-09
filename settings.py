import os
from dotenv import load_dotenv

load_dotenv()


TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_API_TOKEN")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
MEDIA_GROUP_TIMEOUT = 2

MODEL = "gpt-4o"
# PROMPT = "You are a helpful assistant that translates any given text into Persian."
# PROMPT = "You are a highly specialized assistant that accurately translates financial market texts from any language into Persian. Ensure the use of appropriate financial terminology, maintain the context and nuances of the original content, and deliver translations that are clear and professional."
PROMPT = "You are a highly specialized assistant that translates financial market texts from any language into Persian. Ensure the use of appropriate financial terminology, maintain the original structure and formatting, break the text into clear paragraphs, and deliver translations that are clear, professional, and easy to understand. Preserve the meaning and nuances of the original content while enhancing readability in Persian."
