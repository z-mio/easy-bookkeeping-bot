from typing import Literal

from sqlalchemy import INTEGER
from sqlalchemy.orm import Mapped, mapped_column

from accounting.database.tables import Bill
from accounting.database.tables.base import Base
import accounting
from accounting.types import OperateType


class Group(Base):
    __tablename__ = "group"
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)  # 组名
    total: Mapped[float] = mapped_column(default=0)  # 总金额
    from_currency: Mapped[str] = mapped_column(nullable=False)  # 默认货币
    to_currency: Mapped[str] = mapped_column(nullable=False)  # 结算货币
    default: Mapped[bool] = mapped_column(
        nullable=False, default=False
    )  # 是否为默认分组

    async def ls(
        self,
        limit: int | None = None,
        order_by_date: Literal["asc", "desc"] = "asc",
        clearing_status: bool = False,
    ) -> list["Bill"]:
        """列出账单"""
        return await accounting.acc.ls_bill(
            self.id, limit, order_by_date, clearing_status
        )

    async def add(
        self,
        money: float,
        operate: "OperateType",
        actual_money: float,
        rate_operate: "OperateType",
        rate: float = 1,
        fee: float = 0,
        remark: str = None,
    ) -> "Bill":
        """添加账单"""
        return await accounting.acc.add_bill(
            money, operate, actual_money, rate_operate, rate, fee, remark, self.id
        )

    async def update_total(self, money: float, operate: Literal["+", "-"]) -> "Group":
        """更新总金额"""
        return await accounting.acc.update_group_total(self.id, money, operate)

    async def clearing(self):
        """清账"""
        return await accounting.acc.group_clearing(self.id)

    async def delete(self) -> "Group":
        """删除分组"""
        return await accounting.acc.delete_group(self.id)

    async def set_as_default(self) -> "Group":
        """设为默认分组"""
        return await accounting.acc.set_as_default_group(self.id)

    async def edit(self, **kwargs) -> "Group":
        """编辑分组"""
        return await accounting.acc.edit_group(self.id, **kwargs)

    async def export(self) -> str:
        """导出账单"""
        return await accounting.acc.export_bill(self.id)

    async def undo_latest(self) -> Bill | None:
        """撤销最近的账单"""
        bill = await accounting.acc.get_latest_bill(self.id)
        if not bill:
            return
        return await bill.delete()
