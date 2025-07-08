import httpx
from loguru import logger


class FeishuClient:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0, connect=10.0),
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10),
        )

    async def send_message(self, content: str, title: str | None = None) -> bool:
        max_retries = 3
        for attempt in range(max_retries):
            try:
                message_data = {
                    "msg_type": "interactive",
                    "card": {
                        "elements": [
                            {
                                "tag": "div",
                                "text": {"content": content, "tag": "lark_md"},
                            }
                        ]
                    },
                }

                if title:
                    message_data["card"]["header"] = {
                        "title": {"content": title, "tag": "plain_text"}
                    }

                response = await self.client.post(
                    self.webhook_url,
                    json=message_data,
                    headers={"Content-Type": "application/json"},
                )

                if response.status_code == 200:
                    result = response.json()
                    if result.get("StatusCode") == 0:
                        logger.debug("消息发送成功到飞书")
                        return True
                    else:
                        logger.error(f"飞书返回错误: {result}")
                        return False
                else:
                    logger.error(f"HTTP错误: {response.status_code} - {response.text}")
                    # 对于4xx错误不重试
                    if 400 <= response.status_code < 500:
                        return False

            except httpx.TimeoutException:
                logger.warning(f"发送消息到飞书超时 (尝试 {attempt + 1}/{max_retries})")
                if attempt == max_retries - 1:
                    logger.error("发送消息到飞书超时，已达最大重试次数")
                    return False
            except httpx.NetworkError as e:
                logger.warning(f"网络错误 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt == max_retries - 1:
                    logger.error("网络错误，已达最大重试次数")
                    return False
            except Exception as e:
                logger.error(f"发送消息到飞书时出错: {e}")
                return False

        return False

    async def close(self):
        try:
            await self.client.aclose()
        except Exception as e:
            logger.error(f"关闭HTTP客户端时出错: {e}")
