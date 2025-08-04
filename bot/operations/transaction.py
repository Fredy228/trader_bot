import MetaTrader5 as mt5
from decimal import Decimal, ROUND_HALF_UP
import pandas as pd
import traceback

from config import START_BALANCE, SYMBOL, DEBUG_MODE, FROM_DATE
from services.round_decimal import round_decimal
from services.logger import logger

balance = Decimal(str(START_BALANCE))

balance_df = pd.DataFrame(columns=["time", "value"])
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

    if trade_contract_size is None or trade_contract_size == 0:
        logger.info(f"Розмір контракту: 1")
        return Decimal("1")

    logger.info(f"Розмір контракту: {trade_contract_size}")

    return Decimal(str(trade_contract_size))


def calc_lot(type="BUY", stop_loss=0, open_price=0):
    global balance, MAX_LOT

    if stop_loss == 0 or open_price == 0:
        raise ValueError("СЛ та open_price дорівнюють 0")

    contract_size = get_contract_size()

    if type == "BUY":
        lot = (balance * Decimal("0.01")) / ((open_price - stop_loss) * contract_size)
        # if lot > MAX_LOT:
        #     return MAX_LOT
        return lot

    if type == "SELL":
        lot = (balance * Decimal("0.01")) / ((stop_loss - open_price) * contract_size)
        # if lot < MAX_LOT * -1:
        #     return MAX_LOT * -1
        return lot


def transaction_test(order, open_price):
    global balance, balances_line, time_line, profit_sum, loss_sum, balance_df

    contract_size = get_contract_size()
    sl_up = round_decimal(order["level_up"], level="0.0000001")
    sl_down = round_decimal(order["level_down"], level="0.0000001")
    open_price_rounded = round_decimal(open_price, level="0.0000001")
    close_price_rounded = round_decimal(order["price"], level="0.0000001")

    try:
        amount = 0
        if order["type"] == "BUY":
            lot = round_decimal(calc_lot("BUY", sl_down, open_price_rounded))
            points = (close_price_rounded - open_price_rounded) * contract_size
            amount = lot * round_decimal(points)
            logger.info(
                f"order: {order["type"]}_{order["id"]}, open: {open_price_rounded}, close: {close_price_rounded} amount: {amount}, lot: {lot}, points: {points}"
            )
        if order["type"] == "SELL":
            lot = round_decimal(calc_lot("SELL", sl_up, open_price_rounded))
            points = (open_price_rounded - close_price_rounded) * contract_size
            amount = lot * round_decimal(points)
            logger.info(
                f"order: {order["type"]}_{order["id"]}, open: {open_price_rounded}, close: {close_price_rounded} amount: {amount}, amount: {amount}, lot: {lot}, points: {points}"
            )

        if amount > 0:
            profit_sum += amount
        else:
            loss_sum += amount

        balance += amount
        is_duplicate = (
            len(balance_df) > 0
            and balance_df.iloc[len(balance_df) - 1]["time"] == order["time"]
        )

        balance_df.loc[len(balance_df) - 1 if is_duplicate else len(balance_df)] = [
            order["time"],
            float(balance),
        ]
        logger.info(f"Баланс: {float(balance)} {order["type"]}_{order["id"]}")

        return True
    except Exception as e:
        logger.error(f"Помилка при виконанні транзакції: {type(e).__name__}: {e}")
        logger.error(traceback.format_exc())
        return False


def get_balance():
    global balance, profit_sum, loss_sum

    return (
        balance.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        Decimal(str(profit_sum)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        Decimal(str(loss_sum)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
    )


def get_time_line_balance():
    global balance_df

    balance_df = balance_df.sort_values(by="time").reset_index(drop=True)

    return balance_df
