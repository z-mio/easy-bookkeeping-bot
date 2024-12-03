from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    ReplyKeyboardRemove,
    CallbackQuery,
)

from accounting import acc
from module.group.utile import group_info, eg_btn
from utiles.filters import is_admin, step_filter
from utiles.step_statu import step
from module.utile import match_group_name, send_keyboard_msg


@Client.on_message(is_admin & filters.command("eg"))
async def edit_group__select_group(_, msg: Message):
    """选择要编辑的分组"""
    await send_keyboard_msg(msg, "**▎请选择要编辑的分组**\n发送 /cc 取消操作")
    step.set_step(msg.from_user.id, "edit_group")


@Client.on_message(is_admin & filters.text & step_filter("edit_group"))
async def edit_group__select_items(_, msg: Message):
    """选择要编辑的项目"""
    group_name = msg.text
    group = await acc.get_group(group_name)
    await (await msg.reply("移除键盘", reply_markup=ReplyKeyboardRemove())).delete()
    await msg.reply(
        group_info(group),
        reply_markup=eg_btn(group),
    )

    step.set_step(msg.from_user.id, "edit_group_items")


@Client.on_callback_query(filters.regex(r"^edit_group"))
async def edit_group__selected(_, cq: CallbackQuery):
    """已选择要编辑的项"""
    item = cq.data.split("|")[1]
    msg = cq.message
    group_name = match_group_name(msg.text)
    if not await acc.get_group(group_name):
        return await msg.reply("**▎分组不存在**", quote=True)

    step.insert(cq.from_user.id, edit_group_name=match_group_name(msg.text))

    c = "发送 /cc 取消操作"
    match item:
        case "name":
            await msg.reply(f"**▎请发送新的分组名**\n{c}")
            step.set_step(cq.from_user.id, "edit_group_name")
        case "from_currency":
            await msg.reply(f"**▎请发送新的默认货币**\n{c}")
            step.set_step(cq.from_user.id, "edit_group_from_currency")
        case "default":
            await edit_group__set_as_default(_, cq)


@Client.on_message(is_admin & filters.text & step_filter("edit_group_name"))
async def edit_group__name(_, msg: Message):
    """编辑分组名"""
    group_name = step.get(msg.from_user.id, "edit_group_name")
    new_group_name = msg.text
    if await acc.get_group(new_group_name):
        return await msg.reply(f"**▎分组已存在:** `{new_group_name}` **请重新发送**")
    await acc.edit_group(group_name, name=new_group_name)
    await msg.reply(
        f"**▎重命名分组:** `{group_name}` -> `{new_group_name}`",
        reply_markup=ReplyKeyboardRemove(),
    )
    step.set_step(msg.from_user.id, "edit_group", False)


@Client.on_message(is_admin & filters.text & step_filter("edit_group_from_currency"))
async def edit_group__from_currency(_, msg: Message):
    """编辑默认货币"""
    group_name = step.get(msg.from_user.id, "edit_group_name")
    from_currency = acc.get_currency(msg.text)
    if not from_currency:
        return await msg.reply("**▎货币不存在, 请重新输入**")
    group = await acc.edit_group(group_name, from_currency=from_currency)
    await msg.reply(
        f"**▎修改默认货币:** `{acc.get_currency_text(group.from_currency)}` -> `{acc.get_currency_text(from_currency)}`",
        reply_markup=ReplyKeyboardRemove(),
    )


async def edit_group__set_as_default(_, cq: CallbackQuery):
    """设为默认分组"""
    msg = cq.message
    group_name = step.get(cq.from_user.id, "edit_group_name")
    group = await acc.set_as_default_group(group_name)
    (await msg.edit_reply_markup(eg_btn(group)),)
    step.set_step(msg.from_user.id, "edit_group", False)
