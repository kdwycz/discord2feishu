import discord


class MessageFormatter:
    @staticmethod
    def format_discord_message(message: discord.Message) -> tuple[str, str]:
        author_name = message.author.display_name
        channel_name = (
            message.channel.name if hasattr(message.channel, "name") else "未知频道"
        )

        title = f"Discord #{channel_name} - {author_name}"

        content = message.content

        if message.attachments:
            attachment_info = "\n\n**附件:**\n"
            for attachment in message.attachments:
                attachment_info += f"- [{attachment.filename}]({attachment.url})\n"
            content += attachment_info

        if message.embeds:
            embed_info = "\n\n**嵌入内容:**\n"
            for embed in message.embeds:
                if embed.title:
                    embed_info += f"**{embed.title}**\n"
                if embed.description:
                    embed_info += f"{embed.description}\n"
                if embed.url:
                    embed_info += f"[链接]({embed.url})\n"
            content += embed_info

        if not content.strip():
            content = "_[此消息没有文本内容]_"

        guild_id = message.guild.id if message.guild else "@me"
        message_link = (
            f"https://discord.com/channels/{guild_id}/{message.channel.id}/{message.id}"
        )
        content += f"\n\n[查看原消息]({message_link})"

        return title, content
