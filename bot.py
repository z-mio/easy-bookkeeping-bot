# -*- coding: UTF-8 -*-

from pyrogram import Client

from config.config import cfg

from accounting.log import logger

logger.add("logs/bot.log", rotation="1 MB")

proxy = (
    {
        "scheme": cfg.proxy.scheme,
        "hostname": cfg.proxy.hostname,
        "port": cfg.proxy.port,
    }
    if cfg.proxy
    else None
)

plugins = dict(root="module")

app = Client(
    "my_bot",
    proxy=proxy,
    bot_token=cfg.bot_token,
    api_id=cfg.api_id,
    api_hash=cfg.api_hash,
    plugins=plugins,
    lang_code="zh",
)

if __name__ == "__main__":
    logger.info("bot开始运行...")
    app.run()
