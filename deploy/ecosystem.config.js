module.exports = {
  apps: [{
    name: 'discord2feishu',
    script: 'uv',
    args: ['run', 'discord2feishu'],
    // 使用当前目录，无需修改路径
    cwd: '.',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '200M',
    // 自动加载 .env 文件
    env_file: '.env',
    // 日志文件使用相对路径
    log_file: './logs/discord2feishu.log',
    out_file: './logs/discord2feishu.out.log',
    error_file: './logs/discord2feishu.error.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
    merge_logs: true,
    log_type: 'json'
  }]
}