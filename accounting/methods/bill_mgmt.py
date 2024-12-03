from accounting.database.tables import Bill
from accounting.types import OperateType, Command
import accounting
from typing import Literal
from accounting.log import logger


class BillMgmt:
    async def add_bill(
        self: "accounting.Accounting",
        money: float,
        operate: OperateType,
        actual_money: float,
        rate_operate: OperateType,
        rate: float = 1,
        fee: float = 0,
        remark: str = None,
        group_id: int = 0,
    ) -> Bill:
        """
        添加账单
        :param money: 金额
        :param operate: 操作类型
        :param actual_money: 实际金额
        :param rate_operate: 汇率操作类型
        :param rate: 汇率
        :param fee: 手续费
        :param remark: 备注
        :param group_id: 分组id
        :return:
        """
        bill = await self.db.add(
            Bill(
                money=money,
                operate=operate,
                actual_money=actual_money,
                rate_operate=rate_operate,
                rate=rate,
                fee=fee,
                remark=remark,
                group_id=group_id,
            )
        )
        await self.update_group_total(
            group_id=bill.group_id, money=bill.actual_money, operate=bill.operate.value
        )
        logger.info(f"添加账单: {(await bill.parse_as_cmd()).raw_cmd}")
        return bill

    async def delete_bill(
        self: "accounting.Accounting", bill_id: int
    ) -> Bill | list[Bill]:
        """删除账单"""
        bill = await self.db.delete(Bill, Bill.id == bill_id)
        await self.update_group_total(bill.group_id, bill.actual_money, "-")
        logger.info(f"删除账单: {bill}")
        return bill

    async def get_bill(self: "accounting.Accounting", bill_id: int) -> Bill:
        """获取账单"""
        return await self.db.get_one(Bill, Bill.id == bill_id)

    async def get_latest_bill(
        self: "accounting.Accounting",
        group: int | str | None = None,
        limit: int | None = 1,
    ) -> Bill | list[Bill]:
        """获取最近账单"""
        k = {"order_by": [Bill.date.desc()], "limit": limit}
        a = []

        if group := await self.get_group(group):
            a.append(Bill.group_id == group.id)
        bills = await self.db.get_all(Bill, *a, **k)
        return bills[0] if limit == 1 else bills

    async def edit_bill(self: "accounting.Accounting", bill_id: int, **kwargs) -> Bill:
        """编辑账单"""
        # old = await self.get_bill(bill_id)
        new = await self.db.update(Bill, Bill.id == bill_id, **kwargs)
        # logger.info(f"编辑账单:\nOld: {old}\nNew: {new}")
        return new

    async def ls_bill(
        self: "accounting.Accounting",
        group: int | str = None,
        limit: int | None = None,
        order_by_date: Literal["asc", "desc"] = "asc",
        clearing_status: bool = False,
    ) -> list[Bill]:
        """获取分组所有账单
        :param group: 分组id
        :param limit: 限制数量
        :param order_by_date: 时间排序方式
        :param clearing_status: 是否已清账
        """

        order_by = [Bill.date.asc()] if order_by_date == "asc" else [Bill.date.desc()]
        arges = [Bill.clearing_status == clearing_status]
        if group and (g := await self.get_group(group)):
            arges.append(Bill.group_id == g.id)
        return await self.db.get_all(
            Bill,
            *arges,
            limit=limit,
            order_by=order_by,
        )

    async def unparse(self: "accounting.Accounting", bill: Bill) -> Command:
        """账单解析为指令"""
        group_name = (await self.get_group(bill.group_id)).name
        cmd = (
            f"{bill.operate.value}{bill.money}{bill.rate_operate.value}{bill.rate}+{bill.fee}"
            + (f"#{bill.remark}" if bill.remark else "")
            + f"@{group_name}"
        )
        return await Command.parse(cmd)
