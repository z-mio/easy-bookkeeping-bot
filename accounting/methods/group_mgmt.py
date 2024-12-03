from pathlib import Path

import pandas as pd
from pandas.io.formats.style import Styler

import accounting
from typing import Literal
from accounting.log import logger
from accounting.database.tables import Group, Bill
from config.config import cfg


class GroupMgmt:
    async def create_group(
        self: "accounting.Accounting",
        group_name: str,
        from_currency: str = None,
        to_currency: str = None,
        default: bool = False,
    ) -> Group:
        """创建分组"""
        if from_currency is None:
            from_currency = cfg.from_currency
        if to_currency is None:
            to_currency = cfg.to_currency

        from_currency = self.get_currency(from_currency)
        to_currency = self.get_currency(to_currency)
        if not from_currency or not to_currency:
            raise ValueError("货币不存在")

        group = await self.db.add(
            Group(
                name=group_name,
                from_currency=from_currency,
                to_currency=to_currency,
                default=default,
            )
        )
        logger.info(f"创建分组: {group}")
        return group

    async def ls_group(self: "accounting.Accounting") -> list[Group]:
        """列出所有分组"""
        return await self.db.get_all(Group)

    async def get_group(self: "accounting.Accounting", group: int | str) -> Group:
        """获取分组"""
        if isinstance(group, str):
            return await self.db.get_one(Group, Group.name == group)
        return await self.db.get_one(Group, Group.id == group)

    async def delete_group(
        self: "accounting.Accounting", group: int | str
    ) -> Group | list[Group]:
        """删除分组"""
        logger.info(f"删除分组: {group}")
        group = await self.get_group(group)
        return await self.db.delete(Group, Group.id == group.id)

    async def edit_group(
        self: "accounting.Accounting", group: int | str, **kwargs
    ) -> Group:
        """编辑分组"""
        group = await self.get_group(group)
        u_group = await self.db.update(Group, Group.id == group.id, **kwargs)
        # logger.info(f"编辑分组:\nOld: {group}\nNew: {u_group}")
        return u_group

    async def update_group_total(
        self: "accounting.Accounting",
        group_id: int,
        money: float,
        operate: Literal["+", "-"],
    ) -> Group:
        """更新分组总金额"""
        group = await self.get_group(group_id)
        total = group.total + money if operate == "+" else group.total - money
        return await self.db.update(Group, Group.id == group_id, total=round(total, 2))

    async def group_clearing(self: "accounting.Accounting", group: int | str):
        """清账"""
        group = await self.get_group(group)
        bill = await self.ls_bill(group.id)
        [await b.edit(clearing_status=True) for b in bill]
        await group.edit(total=0)
        logger.info(f"清账: {group.name}")

    async def get_default_group(self: "accounting.Accounting") -> Group:
        """获取默认分组"""
        return await self.db.get_one(Group, Group.default == 1)

    async def set_as_default_group(
        self: "accounting.Accounting", group: int | str
    ) -> Group:
        """设为默认分组"""
        default = await self.get_default_group()
        if default:
            await self.edit_group(default.id, default=False)
        return await self.edit_group(group, default=True)

    @staticmethod
    async def _generate_worksheet(bills: list[Bill]) -> Styler:
        data = {
            "日期": [],
            "操作": [],
            "金额": [],
            "汇率操作": [],
            "汇率": [],
            "手续费": [],
            "实际金额": [],
            "备注": [],
        }
        for b in bills:
            data["日期"].append(b.date)
            data["操作"].append(b.operate.value)
            data["金额"].append(b.money)
            data["汇率操作"].append(b.rate_operate.value)
            data["汇率"].append(b.rate)
            data["手续费"].append(b.fee)
            data["实际金额"].append(b.actual_money)
            data["备注"].append(b.remark)
        df = pd.DataFrame(data)
        return df.style.set_properties(**{"text-align": "center"})

    async def export_bill(
        self: "accounting.Accounting",
        group: int | str | None,
        path: str | Path = "账单.xlsx",
    ) -> str:
        """导出账单, 不传group则导出所有账单"""

        groups = [await self.get_group(group)] if group else await self.ls_group()
        dfs = {}
        for g in groups:
            bill = await self.ls_bill(g.id)
            df = await self._generate_worksheet(bill)
            dfs[g.name] = df

        with pd.ExcelWriter(path, engine="xlsxwriter") as writer:
            for group_name, df in dfs.items():
                df.to_excel(writer, sheet_name=group_name, index=False)
                worksheet = writer.sheets[group_name]
                worksheet.set_column("A:A", 20)
        return path
