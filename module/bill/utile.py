from accounting import acc
from accounting.types import Command


def bill_format_as_tg(cmd: Command) -> str:
    return (
        f"**{cmd.operate} {cmd.money} {cmd.rate_operate} {cmd.rate}"
        + (f" + {cmd.fee} {cmd.rate_operate} {cmd.rate}" if cmd.fee else "")
        + f" = {cmd.actual_money}**"
        + (f" #{cmd.remark}" if cmd.remark else "")
        + (
            f"\n▎`{acc.rate_equation(cmd.from_currency, cmd.group.to_currency, cmd.rate)}`"
            if cmd.from_currency != cmd.group.to_currency
            and cmd.from_currency != cmd.group.from_currency
            else ""
        )
    )
