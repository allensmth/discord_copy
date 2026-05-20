import discord
from discord.ext import commands

class Example(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="test")
    async def test_command(self, ctx):
        """测试命令示例"""
        embed = discord.Embed(
            title="测试命令",
            description="这是一个示例Cog命令",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        """监听所有消息的示例"""
        if message.author == self.bot.user:
            return
        
        if "hello bot" in message.content.lower():
            await message.reply("你好！", mention_author=False)

async def setup(bot):
    await bot.add_cog(Example(bot))
