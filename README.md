# Discord Self Bot

使用 [discord.py-self](https://discordpy-self.readthedocs.io/en/latest/) 框架构建的自托管Discord机器人。

## 功能特性

- ✅ 使用discord.py-self框架
- ✅ 命令系统（Command）
- ✅ Cogs模块化系统
- ✅ 事件监听
- ✅ 环境变量配置

## 安装

### 前置要求

- Python 3.8+
- pip

### 设置步骤

1. **克隆仓库**
```bash
git clone https://github.com/allensmth/discord_copy.git
cd discord_copy
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境变量**
```bash
cp .env.example .env
```

编辑 `.env` 文件，添加你的Discord用户令牌：
```
DISCORD_TOKEN=your_token_here
```

> ⚠️ **重要**: discord.py-self 是用来创建自托管机器人的，令牌是你的个人账户令牌。请妥善保管，不要分享给任何人！

4. **运行机器人**
```bash
python main.py
```

## 项目结构

```
discord_copy/
├── main.py           # 主机器人文件
├── config.py         # 配置管理
├── requirements.txt  # 依赖列表
├── .env.example      # 环境变量示例
├── .env              # 环境变量（本地，不提交）
└── cogs/
    └── example.py    # 示例Cog模块
```

## 使用方法

### 基础命令

机器人内置以下命令（假设命令前缀为 `!`）：

- `!ping` - 返回机器人延迟
- `!hello` - 发送问候消息
- `!test` - 测试命令示例

### 创建新的Cog

在 `cogs/` 目录下创建新的Python文件：

```python
import discord
from discord.ext import commands

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mycommand")
    async def my_command(self, ctx):
        """我的命令"""
        await ctx.send("Hello!")

async def setup(bot):
    await bot.add_cog(MyCog(bot))
```

Cogs会自动被加载。

## API 文档

更多信息请访问官方文档：
- [discord.py-self 官方文档](https://discordpy-self.readthedocs.io/en/latest/)
- [Discord API 文档](https://discord.com/developers/docs)

## 注意事项

⚠️ **使用discord.py-self的注意事项：**

1. 这是一个用于自托管机器人的库（使用个人账户令牌）
2. 不遵守Discord ToS的风险：自托管机器人可能违反Discord服务条款
3. 账户安全：妥善保管你的令牌，永远不要分享
4. 账户风险：不当使用可能导致账户被封
5. 建议使用专用账户进行测试

## 许可证

MIT

## 贡献

欢迎提交问题和拉取请求。

## 联系方式

如有问题，请提交Issue。

- Forward messages from multiple source channels
- Preserves message author name and avatar
- Forwards attachments (images, files)
- Forwards embeds
- Handles @everyone/@here mentions safely
- Supports unlimited channel mappings
