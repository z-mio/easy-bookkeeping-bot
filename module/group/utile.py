from pyrogram.types import InlineKeyboardMarkup as Ikm, InlineKeyboardButton as Ikb

from accounting import acc
from accounting.database.tables import Group


def group_info(group: Group):
    """分组信息"""
    return (
        f"**▎分组:** `{group.name}`"
        f"\n**▎默认货币:** `{acc.get_currency_text(group.from_currency)}`"
        f"\n**▎结算货币:** `{acc.get_currency_text(group.to_currency)}`"
    )


def eg_btn(group: Group):
    """编辑分组按钮"""
    return Ikm(
        [
            [
                Ikb("修改分组名", "edit_group|name"),
                Ikb("修改默认货币", "edit_group|from_currency"),
            ],
            [
                (
                    Ikb("设为默认分组", "edit_group|default")
                    if not group.default
                    else Ikb("📌默认分组", "默认分组")
                )
            ],
        ]
    )
