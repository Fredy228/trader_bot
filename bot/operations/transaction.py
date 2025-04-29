import MetaTrader5 as mt5
from decimal import Decimal, ROUND_HALF_UP

from config import START_BALANCE, SYMBOL, DEBUG_MODE

balance = Decimal(str(START_BALANCE))

balances_line = []
time_line = []
trade_contract_size = None


def get_contract_size():
    global trade_contract_size

    if trade_contract_size != None:
        return trade_contract_size

    symbol_info = mt5.symbol_info(SYMBOL)

    if symbol_info is None:
        raise ValueError("Символ не найден.")

    print(f"contract_size: {symbol_info.trade_contract_size}")
    trade_contract_size = Decimal(str(symbol_info.trade_contract_size))

    return trade_contract_size


def calc_lot(type="BUY", stop_loss=0, open_price=0):
    global balance

    contract_size = get_contract_size()

    if type == "BUY":
        points = (stop_loss - open_price) * contract_size
        lot = points * (
            (balance * Decimal("0.01")) / ((stop_loss - open_price) * contract_size)
        )
        return lot
    elif type == "SELL":
        points = (open_price - stop_loss) * contract_size
        lot = points * (
            (balance * Decimal("0.01")) / ((open_price - stop_loss) * contract_size)
        )
        return lot
    else:
        raise ValueError("Не верный тип ордера. Используй 'BUY' или 'SELL'.")


def transaction_test(order, open_price):
    global balance, balances_line, time_line

    if order["type"] == "BUY":
        lot = calc_lot("BUY", order["level_down"], open_price)
        amount = lot * (order["price"] - open_price)
        balance += amount
        balances_line.append(balance.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
        time_line.append(order["time"])
    elif order["type"] == "SELL":
        lot = calc_lot("SELL", order["level_up"], open_price)
        amount = lot * (open_price - order["price"])
        balance += amount
        balances_line.append(balance.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
        time_line.append(order["time"])


def get_balance():
    global balance, balances_line

    if DEBUG_MODE == 1:
        print(balances_line)

    return balance.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def get_time_line_balance():
    global time_line, balances_line

    return time_line, balances_line
