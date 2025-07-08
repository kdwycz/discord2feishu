# Discord2Feishu

一个将Discord频道消息自动转发到飞书的机器人，使用现代Python技术栈构建。

## 功能特点

- 🤖 监听指定Discord频道的消息
- 📡 自动转发到飞书群聊webhook
- 🎨 支持富文本格式（Markdown）转换
- 📎 支持附件和嵌入内容转发
- 📝 完整的日志记录和文件轮转
- 🔄 网络错误自动重试
- ⚡ 优雅的启动和关闭处理
- 🛡️ 生产环境就绪的错误处理

## 环境要求

- Python 3.13+
- uv (推荐) 或 pip

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/kdwycz/discord2feishu
cd discord2feishu
```

### 2. 安装依赖

```bash
# 使用 uv (推荐)
uv sync

# 或使用 pip
pip install -e .
```

### 3. 配置环境变量

复制配置模板：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入以下配置：

```env
# Discord Bot Token
DISCORD_TOKEN=your_discord_bot_token_here

# Discord 频道ID
DISCORD_CHANNEL_ID=your_channel_id_here

# 飞书 Webhook URL
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/your_webhook_token_here

# 日志级别 (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO
```

### 4. 运行机器人

```bash
# 使用 uv
uv run discord2feishu

# 或直接运行
python -m discord2feishu.main
```

## 配置指南

### Discord Bot 创建和配置

1. **创建 Discord 应用**
   - 访问 [Discord Developer Portal](https://discord.com/developers/applications)
   - 点击 "New Application" 创建新应用
   - 填写应用名称

2. **创建机器人**
   - 在左侧菜单选择 "Bot"
   - 点击 "Add Bot"
   - 复制 Token 到 `.env` 文件的 `DISCORD_TOKEN`

3. **设置权限**
   - 在左侧菜单选择 "OAuth2" > "URL Generator"
   - **Scopes**: 选择 `bot`
   - **Bot Permissions**: 选择以下权限：
     - ✅ View Channels (查看频道)
     - ✅ Read Message History (读取消息历史)
     - ✅ Manage Messages (管理消息) - 可选，用于删除机器人自己的消息

4. **邀请机器人到服务器**
   - 复制生成的邀请链接
   - 在浏览器中打开，选择要添加机器人的服务器
   - 授权机器人权限

5. **获取频道ID**
   - 在Discord中启用开发者模式：用户设置 > 高级 > 开发者模式
   - 右键点击要监听的频道，选择"复制频道ID"
   - 将ID填入 `.env` 文件的 `DISCORD_CHANNEL_ID`

### 飞书 Webhook 配置

1. **创建飞书群聊**
   - 创建一个新的群聊或使用现有群聊

2. **添加机器人**
   - 在群聊中点击右上角设置
   - 选择"机器人" > "添加机器人"
   - 选择"自定义机器人"

3. **配置 Webhook**
   - 设置机器人名称和描述
   - 复制生成的 Webhook URL
   - 将URL填入 `.env` 文件的 `FEISHU_WEBHOOK_URL`

## 生产环境部署

### 使用 Supervisor (推荐)

Supervisor 提供了稳定的进程管理和自动重启功能。

1. **安装 Supervisor**：
```bash
# Ubuntu/Debian
sudo apt install supervisor

# CentOS/RHEL
sudo yum install supervisor
```

2. **复制并修改配置文件**：
```bash
# 复制配置模板
sudo cp deploy/supervisor.conf /etc/supervisor/conf.d/discord2feishu.conf

# 编辑配置文件，修改以下内容：
# - /path/to/discord2feishu -> 你的项目实际路径
# - app -> 实际运行用户
sudo nano /etc/supervisor/conf.d/discord2feishu.conf
```

3. **启动服务**：
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start discord2feishu
```

4. **管理服务**：
```bash
# 查看状态
sudo supervisorctl status discord2feishu

# 重启服务
sudo supervisorctl restart discord2feishu

# 查看日志
sudo tail -f /var/log/supervisor/discord2feishu.log
```

### 使用 Systemd

Systemd 是现代 Linux 系统的标准服务管理器。

1. **复制并修改配置文件**：
```bash
# 复制配置模板
sudo cp deploy/systemd.service /etc/systemd/system/discord2feishu.service

# 编辑配置文件，修改路径和用户
sudo nano /etc/systemd/system/discord2feishu.service
```

2. **启动和启用服务**：
```bash
sudo systemctl daemon-reload
sudo systemctl enable discord2feishu  # 开机自启
sudo systemctl start discord2feishu
```

3. **管理服务**：
```bash
# 查看状态
sudo systemctl status discord2feishu

# 重启服务
sudo systemctl restart discord2feishu

# 查看日志
sudo journalctl -u discord2feishu -f
```

### 使用 PM2 (Node.js 环境)

如果你的服务器已有 Node.js 环境，PM2 是另一个优秀选择。

1. **安装 PM2**：
```bash
npm install -g pm2
```

2. **直接启动**（无需修改配置文件）：
```bash
# 在项目目录下直接启动
pm2 start deploy/ecosystem.config.js

# 或者复制配置文件到项目根目录
cp deploy/ecosystem.config.js .
pm2 start ecosystem.config.js
```

3. **管理和开机自启**：
```bash
# 查看状态
pm2 status

# 查看日志
pm2 logs discord2feishu

# 重启
pm2 restart discord2feishu

# 设置开机自启
pm2 startup
pm2 save
```

**PM2 优势**：
- 配置文件使用相对路径，无需修改
- 自动读取 `.env` 文件
- 内置日志管理和轮转
- 零停机重启和集群模式

### 使用 Docker

Docker 部署最简单，已包含完整的运行环境，默认配置自动重启。

1. **使用 docker compose**（推荐）：
```bash
# 确保 .env 文件已配置
cp .env.example .env
# 编辑 .env 文件

# 启动（自动构建镜像）
docker compose up -d

# 查看状态和日志
docker compose ps
docker compose logs -f
```

2. **手动构建和运行**：
```bash
# 构建镜像
docker build -t discord2feishu .

# 运行容器（使用.env文件）
docker run -d \
  --name discord2feishu \
  --restart unless-stopped \
  --env-file .env \
  discord2feishu
```

3. **Docker 管理命令**：
```bash
# 查看状态
docker compose ps
# 或
docker ps

# 查看日志
docker compose logs -f discord2feishu
# 或  
docker logs -f discord2feishu

# 重启
docker compose restart
# 或
docker restart discord2feishu

# 停止
docker compose down
# 或
docker stop discord2feishu
```

## 日志管理

### 容器环境（Docker）
机器人默认输出到标准输出，Docker 会自动管理日志轮转。

### 非容器环境（Supervisor/PM2）
- **Supervisor**: 日志由 Supervisor 管理，在配置文件中设置轮转策略
- **PM2**: 自动管理日志文件和轮转
- **手动管理**: 设置环境变量 `LOG_FILE=/path/to/logfile.log` 输出到文件

日志级别可通过环境变量 `LOG_LEVEL` 控制（DEBUG, INFO, WARNING, ERROR）。

## 开发

### 代码格式化

项目使用 ruff 进行代码格式化和检查：

```bash
# 检查代码
uv run ruff check discord2feishu/

# 自动修复
uv run ruff check --fix discord2feishu/

# 格式化代码
uv run ruff format discord2feishu/
```

### 项目结构

```
discord2feishu/
├── discord2feishu/
│   ├── __init__.py
│   ├── main.py          # 主入口和信号处理
│   ├── bot.py           # Discord机器人逻辑
│   ├── config.py        # 配置管理
│   ├── feishu_client.py # 飞书API客户端
│   └── message_formatter.py # 消息格式转换
├── deploy/              # 部署配置文件模板
│   ├── supervisor.conf  # Supervisor配置
│   ├── systemd.service  # Systemd服务配置
│   ├── ecosystem.config.js # PM2配置
│   └── README.md        # 部署说明
├── .env.example         # 环境变量模板
├── docker compose.yml   # Docker Compose配置
├── Dockerfile           # Docker镜像构建文件
├── .gitignore
├── pyproject.toml       # 项目配置
└── README.md
```

## 常见问题

### Q: 机器人无法连接到Discord

A: 检查以下几点：
- Discord Token 是否正确
- 机器人是否已添加到服务器
- 网络连接是否正常

### Q: 消息没有转发到飞书

A: 检查以下几点：
- 飞书 Webhook URL 是否正确
- 频道ID是否正确
- 机器人是否有查看该频道的权限
- 查看日志文件中的错误信息

### Q: 如何查看运行状态

A: 查看日志文件：

```bash
# 查看最新日志
tail -f logs/discord2feishu.log

# 查看错误日志
tail -f logs/errors.log
```

### Q: 如何停止机器人

A: 使用 Ctrl+C 发送 SIGINT 信号，机器人会优雅地关闭所有连接。

### Q: 机器人占用资源过多

A: 机器人设计为轻量级运行，正常情况下内存占用应在100MB以内。如果占用过多，请检查日志中是否有异常。

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 更新日志

### v0.1.0 (2025-07-08)

- 初始版本发布
- 支持Discord消息转发到飞书
- 支持富文本和附件转发
- 完整的日志系统
- 生产环境就绪的错误处理