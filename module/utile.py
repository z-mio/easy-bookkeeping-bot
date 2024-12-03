import re

from config.config import cfg
from utiles.step_statu import step
from pyrogram.types import KeyboardButton as Kb, ReplyKeyboardMarkup as Rkm, Message
from accounting import acc


async def build_group_keyboard(
    msg: Message, hide_default: bool = False, hide_all: bool = True
) -> Rkm:
    """构建分组键盘
    :param msg: 消息对象
    :param hide_default: 是否隐藏默认分组, 默认不隐藏
    :param hide_all: 是否隐藏 "全部" 键, 默认隐藏
    """
    groups = await acc.ls_group()
    if not groups:
        step.init(msg.from_user.id)
        return Rkm(
            [["/cg"]],
            placeholder="暂无分组, 发送 /cg 创建",
            resize_keyboard=True,
            selective=True,
            one_time_keyboard=True,
        )
    all_key = [] if hide_all else [[Kb("全部")]]
    keyboard = [
        Kb(group.name) for group in groups if not hide_default or not group.default
    ]
    keyboard = all_key + [keyboard[i : i + 3] for i in range(0, len(keyboard), 3)]
    return Rkm(
        keyboard,
        resize_keyboard=True,
        selective=True,
        one_time_keyboard=True,
    )


async def build_group_text(
    msg: Message, hide_default: bool = False, hide_all: bool = True
) -> str:
    """构建分组文本
    :param msg: 消息对象
    :param hide_default: 是否隐藏默认分组, 默认不隐藏
    :param hide_all: 是否隐藏 "全部" 键, 默认隐藏
    """
    groups = await acc.ls_group()
    if not groups:
        step.init(msg.from_user.id)
        return "暂无分组, 发送 /cg 创建"
    all_key = [] if hide_all else ["全部"]
    keyboard = [
        f"`{group.name}`" for group in groups if not hide_default or not group.default
    ]
    keyboard = all_key + keyboard
    return "\n".join(keyboard)


async def send_keyboard_msg(
    msg: Message, text: str, hide_default: bool = False, hide_all: bool = True
):
    """根据配置发送消息"""
    if cfg.is_web_telegram and msg.chat.type.name != "PRIVATE":
        await msg.reply(
            f"{text}\n\n**▎分组:**\n{await build_group_text(msg, hide_default, hide_all)}"
        )
    else:
        await msg.reply(
            text=text,
            reply_markup=await build_group_keyboard(msg, hide_default, hide_all),
        )


def match_group_name(text: str):
    return (r := re.search(r"^分组: (.*) 总金额|分组: (.*)", text)) and (
        r.group(1) or r.group(2)
    )
