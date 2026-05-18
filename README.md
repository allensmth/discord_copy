# Discord Message Forwarder

A Python self-bot that forwards messages from multiple source Discord channels to target Discord servers via webhooks.

## ⚠️ Important Note

Using self-bots violates Discord's Terms of Service. Use this at your own risk.

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Edit `config.json`:

```json
{
    "user_token": "YOUR_DISCORD_USER_TOKEN_HERE",
    "channel_mappings": {
        "123456789012345678": "https://discord.com/api/webhooks/...",
        "987654321098765432": "https://discord.com/api/webhooks/..."
    }
}
```

### How to get:

1. **Discord User Token**:
   - Open Discord in browser
   - Press F12 -> Application -> Local Storage -> https://discord.com
   - Find `token` key

2. **Channel ID**:
   - Enable Developer Mode in Discord settings
   - Right-click channel -> Copy ID

3. **Webhook URL**:
   - Go to target server -> Server Settings -> Integrations -> Webhooks
   - Create new webhook -> Copy URL

## Usage

```bash
python forwarder.py
```

## Features

- Forward messages from multiple source channels
- Preserves message author name and avatar
- Forwards attachments (images, files)
- Forwards embeds
- Handles @everyone/@here mentions safely
- Supports unlimited channel mappings
