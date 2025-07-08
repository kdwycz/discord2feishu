FROM python:3.13-slim

# 设置工作目录
WORKDIR /app

# 安装 uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 设置环境变量
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1

# 复制项目配置文件
COPY pyproject.toml ./

# 复制源代码
COPY discord2feishu/ ./discord2feishu/

# 安装依赖
RUN uv sync --no-dev

# 创建非root用户
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# 运行应用
CMD ["uv", "run", "discord2feishu"]