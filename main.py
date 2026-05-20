import discord
from discord.ext import commands
import os
from config import DISCORD_TOKEN

# 创建bot实例
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, self_bot=True)

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    print(f"Bot ID: {bot.user.id}")

@bot.command(name="ping")
async def ping(ctx):
    """发送一个ping命令来检查bot是否在线"""
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

@bot.command(name="hello")
async def hello(ctx):
    """发送一个简单的问候"""
    await ctx.send(f"Hello {ctx.author.name}!")

async def load_cogs():
    """加载所有cogs"""
    cogs_dir = "cogs"
    if os.path.exists(cogs_dir):
        for filename in os.listdir(cogs_dir):
            if filename.endswith(".py"):
                try:
                    await bot.load_extension(f"cogs.{filename[:-3]}")
                    print(f"已加载 cog: {filename}")
                except Exception as e:
                    print(f"加载 cog {filename} 失败: {e}")

async def main():
    """启动bot"""
    async with bot:
        await load_cogs()
        await bot.start(DISCORD_TOKEN, bot=False)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
