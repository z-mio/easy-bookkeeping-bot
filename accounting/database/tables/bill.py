from datetime import datetime

from sqlalchemy import INTEGER, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from accounting.database.tables.base import Base
from accounting.types import OperateType, DBOperateType, Command
import accounting


class Bill(Base):
    __tablename__ = "bill"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    operate: Mapped[OperateType] = mapped_column(DBOperateType)  # 操作类型
    money: Mapped[float]  # 金额
    rate_operate: Mapped[OperateType] = mapped_column(DBOperateType)  # 汇率操作类型
    rate: Mapped[float]  # 汇率
    fee: Mapped[float]  # 手续费
    actual_money: Mapped[float]  # 实际金额
    remark: Mapped[str] = mapped_column(nullable=True)  # 备注
    clearing_status: Mapped[bool] = mapped_column(default=False)  # 清账
    date: Mapped[datetime] = mapped_column(default=datetime.now())  # 日期
    group_id: Mapped[int] = mapped_column(INTEGER, ForeignKey("group.id"))  # 分组ID

    async def parse_as_cmd(self) -> Command:
        """解析为命令"""
        return await accounting.acc.unparse(self)

    async def edit(self, **kwargs) -> "Bill":
        """编辑账单"""
        return await accounting.acc.edit_bill(self.id, **kwargs)

    async def delete(self) -> "Bill":
        """删除账单"""
        return await accounting.acc.delete_bill(self.id)
