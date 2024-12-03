from pyrogram import filters
from pyrogram.types import Message
from config.config import cfg

from utiles.step_statu import StepStatu

is_admin = filters.chat(cfg.available_chat)


def step_filter(step: str):
    """步骤过滤器"""

    def func(_, __, msg: Message):
        if not msg.from_user:
            return False
        return StepStatu().step_statu(
            msg.from_user.id, step
        ) and not msg.text.startswith("/")

    return filters.create(func)


async def _use_tips_group(_, __, msg: Message):
    """在群组中使用提示"""
    if msg.chat.type.value not in ["group", "supergroup"]:
        await msg.reply("**▎请在群组中使用此命令!**")
        return False
    return True


use_tips_group = filters.create(_use_tips_group)
