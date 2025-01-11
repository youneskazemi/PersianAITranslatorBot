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

MODEL = os.environ.get("MODEL", "gpt-4o-mini")
PROMPT = os.environ.get("PROMPT")
