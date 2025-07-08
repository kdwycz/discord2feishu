import discord
from discord.ext import commands
from loguru import logger

from .config import Config
from .feishu_client import FeishuClient
from .message_formatter import MessageFormatter


class Discord2FeishuBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

        self.feishu_client = FeishuClient(Config.FEISHU_WEBHOOK_URL)
        self.target_channel_id = Config.DISCORD_CHANNEL_ID

    async def on_ready(self):
        logger.info(f"机器人已登录: {self.user}")
        channel = self.get_channel(self.target_channel_id)
        if channel:
            logger.info(f"监听频道: #{channel.name} (ID: {channel.id})")
        else:
            logger.error(f"无法找到频道ID: {self.target_channel_id}")

    async def on_disconnect(self):
        logger.warning("与Discord连接断开")

    async def on_resumed(self):
        logger.info("Discord连接已恢复")

    async def on_error(self, event, *args, **kwargs):
        logger.exception(f"Discord事件 {event} 发生错误")

    async def on_message(self, message: discord.Message):
        try:
            if message.author == self.user:
                return

            if message.channel.id != self.target_channel_id:
                return

            content_preview = (
                message.content[:50] if message.content else "[无文本内容]"
            )
            logger.info(
                f"收到来自 {message.author.display_name} 的消息: {content_preview}..."
            )

            title, content = MessageFormatter.format_discord_message(message)

            success = await self.feishu_client.send_message(content, title)
            if success:
                logger.info("消息已转发到飞书")
            else:
                logger.error("转发消息到飞书失败")
        except Exception as e:
            logger.exception(f"处理消息时出错: {e}")

    async def close(self):
        logger.info("正在关闭Discord连接...")
        try:
            await self.feishu_client.close()
        except Exception as e:
            logger.error(f"关闭飞书客户端时出错: {e}")

        try:
            await super().close()
        except Exception as e:
            logger.error(f"关闭Discord连接时出错: {e}")
