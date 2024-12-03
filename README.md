# easy-accounting-bot

---

一个简单的Tg记账bot

### 修改配置

将 `.env.example` 复制为 `.env`, 并修改配置

| 参数                   | 说明                            |
|----------------------|-------------------------------|
| `API_HASH`, `API_ID` | 登录 https://my.telegram.org 获取 |
| `BOT_TOKEN`          | 在 @BotFather 获取               |
| `AVAILABLE_CHAT`     | Bot白名单, 可以填用户id,群组id          |
| `FROM_CURRENCY`      | 默认货币                          |
| `TO_CURRENCY`        | 默认结算货币                        |
| `PROXY`              | 代理地址, 海外服务器不用填                |

### 开始部署

**在项目根目录运行:**

```shell
apt install python3-pip -y
pip install uv --break-system-packages
uv venv --python 3.10
uv sync
```

**启动bot**

```shell
uv run bot.py
```

**设置命令列表**
私聊bot发送指令 `/menu`
