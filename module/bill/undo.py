from pyrogram import filters, Client
from pyrogram.types import Message

from module.bill.utile import bill_format_as_tg
from utiles.filters import is_admin
from accounting import acc


@Client.on_message(is_admin & filters.command("un"))
async def undo_bill(_, msg: Message):
    """撤回账单"""
    bill = await acc.get_latest_bill()
    if not bill:
        return await msg.reply("**▎没有账单**")
    await bill.delete()
    group = await acc.get_group(bill.group_id)
    text = (
        f"**分组: `{group.name}` 总金额:** `{group.total}` `{group.to_currency.upper()}`"
        + f"\n**▎已撤回:** {bill_format_as_tg(await bill.parse_as_cmd())}"
    )
    await msg.reply(text)
