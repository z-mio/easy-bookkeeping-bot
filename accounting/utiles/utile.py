import re
from typing import Union


def number_format(number: float) -> Union[int, float]:
    """数字格式化, 去除为0的小数"""
    if number.is_integer():
        return int(number)
    return round(number, 2)


def re_cmd(pattern: str, cmd: str, i: int = 1):
    return (r := re.search(pattern, cmd)) and r[i]
