# easy-accounting-bot
---

一个简单的Tg记账bot

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