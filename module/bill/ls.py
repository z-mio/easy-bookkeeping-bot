import os

from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardRemove

from accounting import acc
from config.config import OP
from module.bill.utile import bill_format_as_tg
from utiles.filters import is_admin, step_filter
from utiles.step_statu import step
from module.utile import send_keyboard_msg


@Client.on_message(is_admin & filters.command("tt"))
async def total(_, msg: Message):
    """所有分组账单汇总"""
    text = "\n".join(
        [
            f"▎**{group.name}:** `{group.total}` `{group.to_currency.upper()}`"
            for group in await acc.ls_group()
        ]
    )
    await msg.reply(text)


@Client.on_message(is_admin & filters.command("ls"))
async def ls_bill__select_group(_, msg: Message):
    """选择分组"""
    await send_keyboard_msg(msg, "**▎请选择分组**\n发送 /cc 取消操作")
    step.set_step(msg.from_user.id, "ls_bill")


@Client.on_message(is_admin & filters.text & step_filter("ls_bill"))
async def ls_bill(_, msg: Message):
    """列出账单"""
    group_name = msg.text
    group = await acc.get_group(group_name)
    if not group:
        return await msg.reply("**▎分组不存在, 请重新选择**")
    limit = 50
    text = f"**分组:** `{group.name}` **总金额:** `{group.total}`\n<u>最近 {limit} 条账单:</u>\n"
    text += "<blockquote expandable>"
    text += "\n".join(
        [
            f"▎{bill_format_as_tg(await bill.parse_as_cmd())}"
            for bill in await group.ls(limit=limit, order_by_date="desc")
        ]
    )
    text += "</blockquote>"

    await msg.reply(text, reply_markup=ReplyKeyboardRemove())
    step.init(msg.from_user.id)


@Client.on_message(is_admin & filters.command("ex"))
async def export_bill__select_group(_, msg: Message):
    """选择分组"""
    await send_keyboard_msg(msg, "**▎请选择分组**\n发送 /cc 取消操作", hide_all=False)
    step.set_step(msg.from_user.id, "export_bill")


@Client.on_message(is_admin & filters.text & step_filter("export_bill"))
async def export_bill(_, msg: Message):
    """导出账单"""
    group = await acc.get_group(msg.text)

    if a := msg.text != "全部" and not group:
        return await msg.reply("**▎分组不存在, 请重新选择**")

    path = await acc.export_bill(group.id if a else None, path=OP.joinpath("账单.xlsx"))
    await msg.reply_document(path, reply_markup=ReplyKeyboardRemove())
    step.init(msg.from_user.id)
    os.remove(path)
