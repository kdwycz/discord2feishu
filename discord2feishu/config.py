import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", 0))
    FEISHU_WEBHOOK_URL = os.getenv("FEISHU_WEBHOOK_URL")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def validate(cls) -> bool:
        missing = []
        if not cls.DISCORD_TOKEN:
            missing.append("DISCORD_TOKEN")
        if not cls.DISCORD_CHANNEL_ID:
            missing.append("DISCORD_CHANNEL_ID")
        if not cls.FEISHU_WEBHOOK_URL:
            missing.append("FEISHU_WEBHOOK_URL")

        if missing:
            raise ValueError(f"缺少必要的环境变量: {', '.join(missing)}")
        return True
