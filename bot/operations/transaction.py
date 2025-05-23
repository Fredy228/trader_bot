import MetaTrader5 as mt5
from decimal import Decimal, ROUND_HALF_UP

from config import START_BALANCE, SYMBOL, DEBUG_MODE, FROM_DATE
from services.round_decimal import round_decimal

balance = Decimal(str(START_BALANCE))

balances_line = []
time_line = []
trade_contract_size = None
profit_sum = 0
loss_sum = 0

balances_line.append(Decimal(str(START_BALANCE)))
time_line.append(FROM_DATE)


def get_contract_size():
    global trade_contract_size

    if trade_contract_size != None:
        return trade_contract_size

    symbol_info = mt5.symbol_info(SYMBOL)

    if symbol_info is None:
        raise ValueError(f"Символ {SYMBOL} не знайден.")

    trade_contract_size = Decimal(str(symbol_info.trade_contract_size))

    return trade_contract_size


def calc_lot(type="BUY", stop_loss=0, open_price=0):
    global balance

    contract_size = get_contract_size()

    if type == "BUY":
        lot = (balance * Decimal("0.01")) / ((open_price - stop_loss) * contract_size)
        return lot

    elif type == "SELL":
        lot = (balance * Decimal("0.01")) / ((stop_loss - open_price) * contract_size)
        return lot

    else:
        raise ValueError("Не вірний тип ордера. Використовуй 'BUY' или 'SELL'.")


def transaction_test(order, open_price):
    global balance, balances_line, time_line, profit_sum, loss_sum

    contract_size = get_contract_size()

    try:
        amount = 0
        if order["type"] == "BUY":
            lot = round_decimal(calc_lot("BUY", order["level_down"], open_price))
            points = (order["price"] - open_price) * contract_size
            amount = lot * round_decimal(points)
            print(f"order: {order['name']}, type: buy, amount: {amount}, lot: {lot}")
        elif order["type"] == "SELL":
            lot = round_decimal(calc_lot("SELL", order["level_up"], open_price))
            points = (open_price - order["price"]) * contract_size
            amount = lot * round_decimal(points)
            print(f"order: {order['name']}, type: sell, amount: {amount}, lot: {lot}")

        if amount > 0:
            profit_sum += amount
        else:
            loss_sum += amount

        balance += amount
        balances_line.append(balance.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
        time_line.append(order["time"])

        return True
    except Exception as e:
        print(f"Помилка при виконанні транзакції: {e}")
        return False


def get_balance():
    global balance, balances_line, profit_sum, loss_sum

    if DEBUG_MODE == 1:
        print(balances_line)

    return (
        balance.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        Decimal(str(profit_sum)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        Decimal(str(loss_sum)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
    )


def get_time_line_balance():
    global time_line, balances_line

    return time_line, balances_line
