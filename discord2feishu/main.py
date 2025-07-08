import asyncio
import os
import signal
import sys

from loguru import logger

from .bot import Discord2FeishuBot
from .config import Config


def setup_logging():
    logger.remove()

    # 统一日志格式
    log_format = (
        "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | "
        "{name}:{function}:{line} - {message}"
    )

    # 控制台日志 - 带颜色
    logger.add(
        sink=sys.stdout,
        level=Config.LOG_LEVEL,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
        colorize=True,
    )

    # 如果设置了日志文件路径，则输出到文件（用于非容器环境）
    log_file = os.getenv("LOG_FILE")
    if log_file:
        logger.add(
            sink=log_file,
            level="INFO",
            format=log_format,
            encoding="utf-8",
        )


async def main():
    try:
        Config.validate()
    except ValueError as e:
        # 在配置日志前就出错了，直接打印
        print(f"配置错误: {e}")
        print("请复制 .env.example 为 .env 并填写正确的配置")
        return

    setup_logging()

    bot = Discord2FeishuBot()
    shutdown_event = asyncio.Event()

    def signal_handler(signum, frame):
        logger.info("收到停止信号，正在关闭...")
        shutdown_event.set()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        logger.info("启动Discord2Feishu机器人...")

        # 启动bot的任务
        bot_task = asyncio.create_task(bot.start(Config.DISCORD_TOKEN))

        # 等待shutdown信号或bot异常退出
        done, pending = await asyncio.wait(
            [bot_task, asyncio.create_task(shutdown_event.wait())],
            return_when=asyncio.FIRST_COMPLETED,
        )

        # 取消未完成的任务
        for task in pending:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

        # 如果是bot任务先完成，可能是异常退出
        if bot_task in done:
            try:
                await bot_task
            except Exception as e:
                logger.error(f"机器人异常退出: {e}")

    except Exception as e:
        logger.error(f"机器人运行错误: {e}")
    finally:
        logger.info("正在关闭机器人...")
        if not bot.is_closed():
            await bot.close()
        logger.info("机器人已关闭")


def cli_main():
    asyncio.run(main())


if __name__ == "__main__":
    cli_main()
