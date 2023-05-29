from enum import Enum, EnumMeta


class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True


class BaseEnum(Enum, metaclass=MetaEnum):
    pass


class Operation(BaseEnum):
    CUMULATE = "cum"
    AVERAGE = "avg"
    LASTDIFF = "lstdff"
    MAX = "max"
    MIN = "min"


class Timescale(BaseEnum):
    YEARLY = "y"
    MONTHLY = "m"
    DAILY = "d"


class DataTrades(BaseEnum):
    BUY_VALUE = "buy_value"
    SELL_VALUE = "sell_value"
    BUY_VOLUME = "buy_volume"
    SELL_VOLUME = "sell_volume"


# Data from views
class CalculatedDataTrades(BaseEnum):
    BALANCE_VALUE = "balance_value"
    BALANCE_VOLUME = "balance_value"
    BUY_PRICE = "buy_price"
    SELL_PRICE = "sell_price"


class CalculatedDataMarketTrades(BaseEnum):
    BUY_PRICE_SPREAD = "buy_price_spread"
    SELL_PRICE_SPREAD = "sell_price_spread"
