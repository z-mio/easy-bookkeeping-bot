from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardRemove

from accounting import acc
from utiles.filters import is_admin, step_filter
from utiles.step_statu import step
from module.utile import send_keyboard_msg


@Client.on_message(is_admin & filters.command("rm"))
async def rm_group__select_group(_, msg: Message):
    """选择要删除的分组"""
    await send_keyboard_msg(
        msg,
        "**▎请选择要删除的分组\n▎注意: 删除分组后, 分组中的账单也会被删除**\n发送 /cc 取消操作",
        hide_all=True,
    )
    step.set_step(msg.from_user.id, "rm_group")


@Client.on_message(is_admin & filters.text & step_filter("rm_group"))
async def rm_group(_, msg: Message):
    """删除分组"""
    group = await acc.delete_group(msg.text)
    await msg.reply(
        f"**▎已删除分组:** `{group.name}`", reply_markup=ReplyKeyboardRemove()
    )
    step.init(msg.from_user.id)
