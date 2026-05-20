# Discord 消息转发器

将Discord频道消息自动转发到多个目标频道的工具。

## 功能特性

- ✅ 支持多源频道转发
- ✅ 保留原作者名称和头像
- ✅ 转发附件（图片、文件）
- ✅ 转发Embed消息
- ✅ 安全处理 @everyone/@here 提及
- ✅ 支持无限频道映射
- ✅ 基于 discord.py-self 框架

## 快速开始

### 前置要求

- Python 3.8+
- pip

### 安装步骤

1. **克隆仓库**
```bash
git clone https://github.com/allensmth/discord_copy.git
cd discord_copy
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置转发器**

编辑 `config.json` 文件：

```json
{
    "user_token": "YOUR_DISCORD_USER_TOKEN_HERE",
    "channel_mappings": {
        "SOURCE_CHANNEL_ID_1": "TARGET_WEBHOOK_URL_1",
        "SOURCE_CHANNEL_ID_2": "TARGET_WEBHOOK_URL_2"
    }
}
```

**配置说明：**
- `user_token`: 你的Discord账户令牌
- `channel_mappings`: 源频道ID到目标Webhook URL的映射
  - 键：源频道ID（数字字符串）
  - 值：目标频道的Webhook URL

### 获取Discord用户令牌

1. 打开Discord桌面端或网页端
2. 按 `F12` 打开开发者工具
3. 进入 **Application** (应用) 标签
4. 在左侧找到 **Local Storage** → `https://discord.com`
5. 搜索 `token` 字段，复制值

> ⚠️ **重要警告**: 用户令牌等同于你的账户密码！
> - 永远不要分享给任何人
> - 不要提交到公开仓库
> - 不当使用可能导致账户被封禁

### 获取频道ID

1. 在Discord设置中开启 **开发者模式**（用户设置 → 高级 → 开发者模式）
2. 右键点击任意频道 → **复制ID**

### 创建Webhook

1. 进入目标频道设置 → **整合** → **Webhook**
2. 点击 **新建Webhook**
3. 复制Webhook URL

### 运行转发器

```bash
python forwarder.py
```

启动成功后会显示：
```
Logged in as [你的用户名]
Monitoring 2 channel(s)
  - #channel-name (ID: 123456789) -> https://discord.com/api/webhooks/...
```

## 工作原理

1. 转发器使用你的账户登录Discord
2. 监听所有配置的源频道
3. 当有新消息时，通过Webhook转发到目标频道
4. 保留原作者信息、附件和Embed

## 注意事项

⚠️ **重要提示：**

1. **Discord服务条款风险**：使用 discord.py-self（自托管机器人）可能违反Discord服务条款
2. **账户安全**：妥善保管你的令牌，永远不要分享
3. **账户风险**：不当使用可能导致账户被封禁
4. **建议使用专用测试账户**

## 项目结构

```
discord_copy/
├── forwarder.py      # 消息转发器主文件
├── config.json       # 配置文件（令牌、频道映射）
├── requirements.txt  # 依赖列表
├── main.py           # 备用机器人入口
├── config.py         # 环境变量配置
├── .env.example      # 环境变量示例
└── cogs/             # Cogs模块化目录
```

## 依赖包

- `discord.py-self` - Discord自托管机器人框架
- `aiohttp` - 异步HTTP客户端

## 故障排除

### 登录失败
- 确认令牌正确
- 检查网络连接
- 确保discord.py-self版本兼容

### 消息不转发
- 确认源频道ID正确
- 确认Webhook URL有效
- 检查控制台是否有错误信息

### 附件转发失败
- 检查文件大小限制（Discord Webhook限制8MB）
- 确认网络连接正常

## 许可证

MIT
