from pyrogram import Client, filters
from pyrogram.types import BotCommand, Message

from utiles.filters import is_admin

COMMANDS = {
    "ls": "账单明细",
    "cg": "创建分组",
    "eg": "编辑分组",
    "rm": "删除分组",
    "tt": "账单汇总",
    "ex": "导出账单",
    "un": "撤回账单",
    "cl": "清空账单",
    "cm": "设置群默认分组",
    "sm": "查看群默认分组",
    "cc": "取消操作",
}


@Client.on_message(filters.command("menu") & filters.private & is_admin)
async def menu(cli: Client, message: Message):
    bot_menu = [BotCommand(command=k, description=v) for k, v in COMMANDS.items()]
    await cli.delete_bot_commands()
    await cli.set_bot_commands(bot_menu)
    await cli.send_message(
        chat_id=message.chat.id, text="菜单设置成功，请重新打开聊天界面"
    )


@Client.on_message(filters.command(["help", "start"]) & is_admin)
async def start(_, msg: Message):
    text = "▎**命令列表:**\n"
    for k, v in COMMANDS.items():
        text += f"▎/{k} - {v}\n"
    await msg.reply(text)
