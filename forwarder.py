import discord
import aiohttp
import json
import re
from typing import Dict, List

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

USER_TOKEN = config['user_token']
CHANNEL_MAPPINGS = config['channel_mappings']

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def clean_mentions(content: str) -> str:
    content = re.sub(r'@everyone', '@​everyone', content)
    content = re.sub(r'@here', '@​here', content)
    return content

async def send_to_webhook(webhook_url: str, message: discord.Message):
    files = []
    for attachment in message.attachments:
        async with aiohttp.ClientSession() as session:
            async with session.get(attachment.url) as resp:
                if resp.status == 200:
                    file_data = await resp.read()
                    files.append(
                        discord.File(
                            fp=file_data,
                            filename=attachment.filename,
                            description=attachment.description
                        )
                    )

    content = clean_mentions(message.content) if message.content else None

    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(webhook_url, session=session)

        embed_data = []
        if message.embeds:
            for embed in message.embeds:
                embed_data.append(embed.to_dict())

        try:
            await webhook.send(
                content=content,
                username=message.author.display_name,
                avatar_url=message.author.avatar.url if message.author.avatar else None,
                files=files if files else None,
                embeds=[discord.Embed.from_dict(e) for e in embed_data] if embed_data else None,
                wait=True
            )
            print(f"Forwarded message from #{message.channel.name} to webhook")
        except Exception as e:
            print(f"Error sending to webhook: {e}")

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    print(f'Monitoring {len(CHANNEL_MAPPINGS)} channel(s)')
    for channel_id, webhook_url in CHANNEL_MAPPINGS.items():
        channel = client.get_channel(int(channel_id))
        if channel:
            print(f'  - #{channel.name} (ID: {channel_id}) -> {webhook_url[:50]}...')

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    channel_id = str(message.channel.id)
    if channel_id in CHANNEL_MAPPINGS:
        webhook_url = CHANNEL_MAPPINGS[channel_id]
        await send_to_webhook(webhook_url, message)

if __name__ == '__main__':
    try:
        client.run(USER_TOKEN)
    except Exception as e:
        print(f"Login error: {e}")
        print("Make sure your user token is valid and you're using the correct library version.")
