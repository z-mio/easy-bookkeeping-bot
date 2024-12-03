from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardRemove
from utiles.step_statu import step


@Client.on_message(filters.command("cc"))
async def cancel(_, msg: Message):
    step.init(msg.from_user.id)
    await msg.reply("**▎已取消操作**", reply_markup=ReplyKeyboardRemove())
