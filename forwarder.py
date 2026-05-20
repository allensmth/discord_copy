import discord
import aiohttp
import io
import json
import re
from typing import Dict, List

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

USER_TOKEN = config['user_token']
CHANNEL_MAPPINGS = config['channel_mappings']

try:
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
except AttributeError:
    # discord.py-self 2.0.1 may not expose discord.Intents.
    client = discord.Client()


def clean_mentions(content: str) -> str:
    content = re.sub(r'@everyone', '@​everyone', content)
    content = re.sub(r'@here', '@​here', content)
    return content

async def send_to_webhook(webhook_url: str, message: discord.Message):
    files = []
    content = clean_mentions(message.content) if message.content else None
    embeds = message.embeds if message.embeds else []
    ref_content = None

    # Handle message references (quoted messages)
    if message.reference and message.reference.message_id:
        try:
            referenced_message = await message.channel.fetch_message(message.reference.message_id)
            if referenced_message:
                ref_text = referenced_message.content[:500] if referenced_message.content else None
                if ref_text:
                    ref_content = f"**Replying to {referenced_message.author.display_name if hasattr(referenced_message.author, 'display_name') else referenced_message.author}:**\n>>> {ref_text}"
                    print(f"Referenced message: {ref_text}")
        except Exception as e:
            print(f"Error fetching referenced message: {e}")

    # Prepend reference to content if it exists
    if ref_content:
        content = f"{ref_content}\n\n{content}" if content else ref_content

    async with aiohttp.ClientSession() as session:
        for attachment in message.attachments:
            try:
                async with session.get(attachment.url) as resp:
                    if resp.status != 200:
                        print(f"Failed to download attachment {attachment.filename}: HTTP {resp.status}")
                        continue

                    file_data = await resp.read()
                    files.append(
                        discord.File(
                            fp=io.BytesIO(file_data),
                            filename=attachment.filename,
                            description=attachment.description
                        )
                    )
            except Exception as e:
                print(f"Error downloading attachment {attachment.filename}: {e}")

        webhook = discord.Webhook.from_url(webhook_url, session=session)

        try:
            kwargs = {
                'username': getattr(message.author, 'display_name', str(message.author)) if message.author else None,
                'allowed_mentions': discord.AllowedMentions.none(),
                'wait': True
            }

            if content:
                kwargs['content'] = content
            if embeds:
                kwargs['embeds'] = embeds
            if files:
                kwargs['files'] = files

            avatar = getattr(message.author, 'avatar', None)
            if avatar:
                kwargs['avatar_url'] = str(avatar.url)

            await webhook.send(**kwargs)
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
