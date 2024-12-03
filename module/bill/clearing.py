from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardRemove

from accounting import acc
from utiles.filters import is_admin, step_filter
from utiles.step_statu import step
from module.utile import send_keyboard_msg


@Client.on_message(is_admin & filters.command("cl"))
async def clearing(_, msg: Message):
    await send_keyboard_msg(msg, "**▎请选择分组**\n发送 /cc 取消操作")
    step.set_step(msg.from_user.id, "clearing")


@Client.on_message(is_admin & filters.text & step_filter("clearing"))
async def clearing_group(_, msg: Message):
    group_name = msg.text
    group = await acc.get_group(group_name)
    if not group:
        return await msg.reply("**▎分组不存在, 请重新选择**")

    await group.clearing()
    await msg.reply(f"**▎已清账:** `{group.name}`", reply_markup=ReplyKeyboardRemove())
    step.init(msg.from_user.id)
