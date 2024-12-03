# easy-bookkeeping-bot

---

一个简单的Tg记账bot

## 功能

**新建分组**  
![](https://img.155155155.xyz/i/2024/12/674eee3d7419d.png)

**记账指令**  
完整指令: `[+-]金额[货币][*/][汇率/货币]+手续费#备注@分组名`  

例:
- `+100`
- `+100usd`
- `+100美元`
- `+100*日元+10#购物`
- `+100@vps`

![](https://img.155155155.xyz/i/2024/12/674efd05654e8.png)

### 修改配置

将 `.env.example` 复制为 `.env`, 并修改配置

| 参数                   | 说明                            |
|----------------------|-------------------------------|
| `API_HASH`, `API_ID` | 登录 https://my.telegram.org 获取 |
| `BOT_TOKEN`          | 在 @BotFather 获取               |
| `AVAILABLE_CHAT`     | Bot白名单, 可以填用户id,群组id, 英文逗号分开  |
| `FROM_CURRENCY`      | 默认货币                          |
| `TO_CURRENCY`        | 结算货币, Bot启动后不可修改              |
| `PROXY`              | 代理地址, 海外服务器不用填                |
| `IS_WEB_TELEGRAM`    | 兼容网页版Tg, 默认关闭                 |

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
