from typing import Union

import accounting.database.tables as tables
from accounting.types import OperateType, Plus, Minus, Times, Divided
from accounting.utiles.utile import number_format as nf
import accounting as acc
from accounting.utiles.utile import re_cmd


class Command:
    def __init__(
        self,
        raw_cmd: str = None,
        money: float = None,
        operate: OperateType = None,
        actual_money: float = None,
        rate_operate: OperateType = None,
        rate: float = None,
        fee: float = None,
        remark: str = None,
        group: "tables.Group" = None,
        from_currency: str = None,
        to_currency: str = None,
    ):
        """

        :param raw_cmd:
        :param money:
        :param operate:
        :param actual_money:
        :param rate_operate:
        :param rate: 汇率
        :param fee:
        :param remark:
        :param group:
        :param from_currency: 货币 例: cny
        :param to_currency: 货币 例: cny
        """
        self.raw_cmd = raw_cmd
        self.money = money
        self.operate = operate
        self.actual_money = actual_money
        self.rate_operate = rate_operate
        self.rate = rate
        self.fee = fee
        self.remark = remark
        self.group = group
        self.from_currency = from_currency
        self.to_currency = to_currency

    @classmethod
    async def parse(cls, cmd: str) -> Union["Command", None]:
        """
        解析记账命令
        完整命令: [+-]金额[货币][*/](汇率/货币)+手续费#备注@分组名
        :param cmd: 命令
        :return:
        """
        cmd = cmd.replace(" ", "").strip()

        if not cmd or not cmd.startswith(("+", "-")):
            return None

        operation_type = Command._parse_operation_type(cmd)
        money = Command._parse_money(cmd)
        group = await Command._parse_group(cmd)
        from_currency, to_currency = Command._parse_currency(cmd, group)
        fee = Command._parse_fee(cmd)
        rate_operation_type, rate = await Command._parse_rate(
            cmd, from_currency, to_currency
        )
        remark = Command._parse_remark(cmd)
        actual_money = Command._calculate_actual_money(
            money, fee, rate, rate_operation_type
        )

        cmd = f"{operation_type}{money}{rate_operation_type}{rate}"
        if fee:
            cmd += f"+{fee}"
        if remark:
            cmd += f"#{remark}"
        if group:
            cmd += f"@{group.name}"

        return cls(
            raw_cmd=cmd,
            money=money,
            operate=operation_type,
            actual_money=actual_money,
            rate_operate=rate_operation_type,
            rate=rate,
            fee=fee,
            remark=remark,
            group=group,
            from_currency=from_currency,
            to_currency=to_currency,
        )

    @staticmethod
    def _parse_operation_type(cmd: str) -> OperateType:
        """操作类型"""
        return Plus() if cmd.startswith("+") else Minus()

    @staticmethod
    def _parse_money(cmd: str) -> float:
        """金额"""
        money_p = r"^[+-]([\d.]*)([^+\-#@*\d]*)"
        if not (money := re_cmd(money_p, cmd)):
            raise AmountIsEmpty()
        return nf(float(money))

    @staticmethod
    async def _parse_group(cmd: str) -> "tables.Group":
        """分组"""
        group_name = (gn := re_cmd(r"@([^+\-#@]*)", cmd)) and gn.lower().strip()
        group = (
            await acc.acc.get_group(group_name)
            if group_name
            else await acc.acc.get_default_group()
        )
        if not group:
            raise GroupDoesNotExist()
        return group

    @staticmethod
    def _parse_currency(cmd: str, group: "tables.Group") -> tuple:
        """货币"""
        money_p = r"^[+-]([\d.]*)([^+\-#@*\d/]*)"
        if not group:
            return group.from_currency, group.to_currency
        return (
            re_cmd(money_p, cmd, 2) or group.from_currency,
            group.to_currency,
        )

    @staticmethod
    def _parse_fee(cmd: str) -> float:
        """手续费"""
        return nf(float(re_cmd(r".\+([\d.]*)\b", cmd) or 0))

    @staticmethod
    async def _parse_rate(
        cmd: str, from_currency: str, to_currency: str
    ) -> tuple[OperateType, float]:
        """汇率"""
        rate_p = r"([*/])([^+\-#@]*)"
        rate_operation_type = Divided() if re_cmd(rate_p, cmd) == "/" else Times()
        rate = re_cmd(rate_p, cmd, 2)

        if rate and rate.replace(".", "").isdigit():  # 指定汇率
            rate = float(rate)
        else:  # 未指定汇率 或 指定货币
            from_currency = acc.acc.get_currency(rate or from_currency)
            if not from_currency:
                raise CurrencyDoesNotExist()

            rate = float(acc.acc.get_rate(from_currency, to_currency))
        return rate_operation_type, nf(rate)

    @staticmethod
    def _parse_remark(cmd: str) -> str:
        """备注"""
        return re_cmd(r"#([^+\-#@]*)", cmd)

    @staticmethod
    def _calculate_actual_money(
        money: float, fee: float, rate: float, rate_operation_type: OperateType
    ) -> float:
        """实际金额"""
        return nf(
            float(
                rate_operation_type.mathematical(money, rate)
                + rate_operation_type.mathematical(fee, rate)
            )
        )


class CommandError(Exception):
    def __init__(self, msg: str):
        self.msg = msg
        super().__init__(msg)


class AmountIsEmpty(CommandError):
    def __init__(self):
        super().__init__("金额为空")


class CurrencyDoesNotExist(CommandError):
    def __init__(self):
        super().__init__("货币不存在")


class GroupDoesNotExist(CommandError):
    def __init__(self):
        super().__init__("分组不存在")
