from accounting.database.tables import Bill
import accounting
from accounting.types import Command


class CommandExecute:
    async def execute(self: "accounting.Accounting", cmd: Command) -> Bill:
        """
        执行记账命令
        :return:
        """

        bill = await self.add_bill(
            money=cmd.money,
            operate=cmd.operate,
            actual_money=cmd.actual_money,
            rate_operate=cmd.rate_operate,
            rate=cmd.rate,
            fee=cmd.fee,
            remark=cmd.remark,
            group_id=cmd.group.id,
        )

        return bill
