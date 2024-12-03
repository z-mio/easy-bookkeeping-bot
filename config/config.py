from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv
from os import getenv

load_dotenv()

OP = Path("data")
OP.mkdir(exist_ok=True, parents=True)


class BotConfig:
    def __init__(self):
        self.available_chat: list[int] | None = (
            list(map(int, getenv("AVAILABLE_CHAT").replace(" ", "").split(","))) or None
        )
        self.bot_token = getenv("BOT_TOKEN")
        self.api_id = getenv("API_ID")
        self.api_hash = getenv("API_HASH")
        self.proxy = (p := getenv("PROXY")) and urlparse(p)

        self.from_currency = getenv("FROM_CURRENCY").lower()
        self.to_currency = getenv("TO_CURRENCY").lower()

        self.is_web_telegram = getenv("IS_WEB_TELEGRAM", "false").lower() == "true"


cfg = BotConfig()
