import os
from dotenv import load_dotenv

load_dotenv()


TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_API_TOKEN")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
MEDIA_GROUP_TIMEOUT = 2

# Authentication settings
ALLOWED_USERS = (
    [int(id) for id in os.environ.get("ALLOWED_USERS", "").split(",")]
    if os.environ.get("ALLOWED_USERS")
    else []
)
ALLOWED_CHANNELS = (
    [int(id) for id in os.environ.get("ALLOWED_CHANNELS", "").split(",")]
    if os.environ.get("ALLOWED_CHANNELS")
    else []
)
ALLOWED_GROUPS = (
    [int(id) for id in os.environ.get("ALLOWED_GROUPS", "").split(",")]
    if os.environ.get("ALLOWED_GROUPS")
    else []
)

MODEL = "gpt-4o"
PROMPT = "You are a highly specialized assistant that translates financial market texts from any language into Persian. Ensure the use of appropriate financial terminology, maintain the original structure and formatting, break the text into clear paragraphs, and deliver translations that are clear, professional, and easy to understand. Preserve the meaning and nuances of the original content while enhancing readability in Persian."
