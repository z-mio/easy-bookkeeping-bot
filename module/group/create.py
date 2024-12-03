from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardRemove

from accounting import acc
from module.group.edit import edit_group__select_items
from utiles.filters import is_admin


@Client.on_message(is_admin & filters.command("cg"))
async def create_group(_, msg: Message):
    """新建分组"""
    if not (cmd := msg.command[1:]):
        return await msg.reply(
            "▎**格式: /cg [分组名] [默认货币] [结算货币]**"
            "<blockquote>`默认货币` 和 `结算货币` 可不填, 默认使用配置文件中的配置</blockquote>"
            "\n▎例: "
            "<blockquote>"
            "`/cg vps`"
            "\n`/cg 机场 cny`"
            "\n`/cg 其他 新加坡 cny`"
            "</blockquote>",
            reply_markup=ReplyKeyboardRemove(),
        )
    if await acc.get_group(cmd[0]):
        return await msg.reply(f"**▎分组已存在:** `{cmd[0]}`")

    try:
        group = await acc.create_group(*cmd, default=not await acc.ls_group())
    except ValueError as e:
        return await msg.reply(f"**▎{e}**")
    msg.text = group.name

    await edit_group__select_items(_, msg)
