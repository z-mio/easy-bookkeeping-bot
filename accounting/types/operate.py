from sqlalchemy import TypeDecorator, String
from sqlalchemy.ext.declarative import declarative_base


class OperateType:
    value = None

    def __repr__(self):
        return self.value

    def mathematical(self, x: int | float, y: int | float):
        match self.value:
            case "+":
                r = x + y
            case "-":
                r = x - y
            case "*":
                r = x * y
            case "/":
                r = x / y
            case _:
                return None
        return round(r, 2)


class Plus(OperateType):
    value = "+"


class Minus(OperateType):
    value = "-"


class Times(OperateType):
    value = "*"


class Divided(OperateType):
    value = "/"


Base = declarative_base()


class DBOperateType(TypeDecorator):
    impl = String
    cache_ok = True
    status_map = {"+": Plus, "-": Minus, "*": Times, "/": Divided}

    def process_bind_param(self, value: OperateType, dialect):
        if value is not None:
            return value.value
        return None

    def process_result_value(self, value, dialect) -> OperateType | None:
        if value is not None:
            return self.status_map.get(value, None)
        return None
