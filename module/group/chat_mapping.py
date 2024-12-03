from pyrogram import Client, filters
from pyrogram.types import Message

from utiles.filters import is_admin, use_tips_group
from accounting import acc
from methods import Methods


@Client.on_message(is_admin & filters.command("cm") & use_tips_group)
async def chat_mapping(_, msg: Message):
    """为群组设置默认使用的分组"""
    chat_id = msg.chat.id
    if not msg.command[1:]:
        return await msg.reply("**▎请加上分组名**\n例: `/cm vps`")
    group = await acc.get_group(msg.command[1])
    if not group:
        return await msg.reply("**▎分组不存在**")
    if await Methods().get_chat_group_mapping(chat_id):
        await Methods().edit_chat_group_mapping(chat_id, group.id)
    else:
        await Methods().add_chat_group_mapping(chat_id, group.id)
    await msg.reply(f"**▎已将本群映射到分组: {group.name}**")


@Client.on_message(is_admin & filters.command("sm") & use_tips_group)
async def show_mapping(_, msg: Message):
    """显示群组默认使用的分组"""
    chat_id = msg.chat.id
    group_mapping = await Methods().get_chat_group_mapping(chat_id)
    if not group_mapping:
        return await msg.reply("**▎本群未映射到分组**")
    group = await acc.get_group(group_mapping.group_id)
    await msg.reply(f"**▎本群已映射到分组: {group.name}**")
