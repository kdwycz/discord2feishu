# 部署配置文件说明

本目录包含各种部署方式的配置文件模板，使用前需要根据实际环境修改路径和用户信息。

## 文件说明

- `supervisor.conf` - Supervisor 进程管理配置
- `ecosystem.config.js` - PM2 进程管理配置  
- `systemd.service` - Systemd 服务配置
- `docker-compose.yml` - Docker Compose 配置（在项目根目录）

## 使用方法

### 1. 配置环境变量

确保项目根目录的 `.env` 文件已正确配置：

```bash
cp .env.example .env
# 编辑 .env 文件填入正确的配置
```

### 2. 选择部署方式

- **PM2**: 直接使用 `pm2 start deploy/ecosystem.config.js`，无需修改配置
- **Supervisor/Systemd**: 复制配置文件并修改路径和用户信息

### 3. 修改配置文件（仅 Supervisor/Systemd）

```bash
# 修改配置文件中的以下内容：
# - /path/to/discord2feishu -> 项目实际路径
# - app -> 实际运行用户
```

### 4. 部署

按照主 README.md 中的部署说明进行操作。

## 注意事项

- 所有配置都已启用开机自启动和自动重启
- 日志文件路径可根据需要调整
- 确保运行用户有足够的权限访问项目目录和日志目录