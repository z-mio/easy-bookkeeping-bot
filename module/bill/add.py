from pyrogram import filters, Client
from pyrogram.types import Message

from accounting import acc
from accounting.types import Command, CommandError
from accounting.types.command import GroupDoesNotExist
from module.bill.utile import bill_format_as_tg
from utiles.filters import is_admin
from module.utile import match_group_name
from methods import Methods


async def bill_cmd_(_, __, msg: Message):
    try:
        return bool(await Command.parse(msg.text))
    except GroupDoesNotExist:
        await msg.reply("▎**分组不存在, 发送 /cg 创建分组**")
        return False
    except CommandError as e:
        await msg.reply(f"▎{e.msg}")
        return False


bill_cmd = filters.create(bill_cmd_)


@Client.on_message(is_admin & filters.regex(r"^[+-]") & bill_cmd)
async def add_bill(_, msg: Message):
    """添加账单"""
    # 使用上一次的分组
    if msg.reply_to_message and "@" not in msg.text:
        group_nmae = match_group_name(msg.reply_to_message.text)
        msg.text += f"@{group_nmae}"
    else:
        if cgm := await Methods().get_chat_group_mapping(msg.chat.id):
            if group := await acc.get_group(cgm.group_id):
                msg.text += f"@{group.name}"

    cmd = await Command.parse(msg.text)
    await acc.execute(cmd)

    text = (
        f"**分组: `{cmd.group.name}` 总金额:** `{(await acc.get_group(cmd.group.name)).total}` `{cmd.group.to_currency.upper()}`"
        + f"\n▎{bill_format_as_tg(cmd)}"
    )
    await msg.reply(text)
