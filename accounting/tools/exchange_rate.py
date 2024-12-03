from datetime import datetime

import httpx

from accounting.utiles.currency_list import currency


class ExchangeRate:
    def __init__(self):
        self.c_r = {}  # {"usd": {"date": "2024-08-04", "usd": {}}}

    @staticmethod
    def get_currency(key: str) -> str:
        """查找货币"""
        key = key.lower()
        currency_ = dict(zip(currency.values(), currency.keys()))
        if currency.get(key):
            return key
        elif currency_.get(key):
            return currency_[key]
        else:
            return (
                i[0]
                if (i := [k for k, v in currency.items() if key in k or key in v])
                else None
            )

    def get_exchange_rate(self, _from: str, _to: str = "cny"):
        """获取汇率"""
        self._check_and_refresh(_from)
        return self.c_r[_from][_from][_to]

    def _check_and_refresh(self, _from):
        """检查时间 刷新汇率"""
        t = datetime.strftime(datetime.now(), "%Y-%m-%d")
        if not (_f := self.c_r.get(_from)) or _f["date"] != t:
            url = f"https://currency-api.pages.dev/v1/currencies/{_from}.json"
            self.c_r[_from] = httpx.get(url).json()

    def get_rate(self, from_key: str, to_key: str) -> float:
        """查找货币 获取汇率"""
        from_ = self.get_currency(from_key)
        to_ = self.get_currency(to_key)
        return self.get_exchange_rate(from_, to_)

    def rate_equation(self, from_: str, to_: str, to_num: float):
        """生成汇率公式"""
        from_, to_ = self.get_currency(from_), self.get_currency(to_)
        return f"1 {from_.upper()}{currency.get(from_)} = {to_num} {to_.upper()}{currency.get(to_)}"

    def get_currency_text(self, key: str) -> str:
        """返回格式: CNY人民币"""
        c = self.get_currency(key)
        return f"{c.upper()}{currency.get(c)}"
