from config import START_BALANCE

from services.logger import logger
from operations.candles import get_candles_from_date
from trade.trade_test_1 import trade_test_1
from operations.show_static_statistic import show_static_statistic
from operations.transaction import get_time_line_balance, get_balance
from statistic.max_drawdown import calc_max_drawdown
from database.repository.archive_orders import get_archive_orders

from config import (
    SYMBOL,
    TIMEFRAME,
    FROM_DATE,
)

_has_shown = False


def test_1():
    global _has_shown
    if _has_shown:
        return
    _has_shown = True

    logger.info("Йде отримання даних...")
    print("\nЙде отримання даних...\n")
    df = get_candles_from_date(SYMBOL, TIMEFRAME, FROM_DATE)
    len_df = len(df)
    print(f"Отримано {len_df} свічок\n")
    logger.info(f"Отримано {len_df} свічок")

    print("\nЙде торгівля...\n")
    logger.info("Йде торгівля...")
    trend = trade_test_1(df)
    balance_history = get_time_line_balance()
    balance, profit_sum, loss_sum = get_balance()
    markers = get_archive_orders()

    profit_orders = [
        m for m in markers if m.get("profit") == 1 and m.get("status") == "CLOSED"
    ]
    loss_orders = [
        m for m in markers if m.get("profit") == 0 and m.get("status") == "CLOSED"
    ]
    cancel_orders = [m for m in markers if m.get("status") == "CANCELED"]

    max_drawdown = calc_max_drawdown(balance_history)

    print("\n\n======= Звіт =======\n")
    print(f"Balance: {START_BALANCE} => {balance}")
    print(f"Profit: {profit_sum}")
    print(f"Loss: {loss_sum}")
    print(f"MDD: {max_drawdown}%")
    print(
        f"\nЗагальна кількість ордерів: {len(profit_orders) + len(loss_orders) + len(cancel_orders)}"
    )
    print(f"Закрито ордерів з профітом: {len(profit_orders)}")
    print(f"Закрито ордерів з втратою: {len(loss_orders)}")
    print(f"Відмінено ордерів: {len(cancel_orders)}")
    print("\n====================\n")

    print("\nЙде будування графіку...\n")
    logger.info("Йде будування графіку...")
    show_static_statistic(
        df,
        trend=trend,
        markers=markers,
        balance_history=balance_history,
    )
