import MetaTrader5 as mt5


def output_account_info():
    account_info = mt5.account_info()

    print(f"Валюта: {account_info.currency}")
    print(f"Поточний баланс: {account_info.balance}")
    print(f"Equity: {account_info.equity}")
    print(f"Credit: {account_info.credit}")
    print(f"Profit: {account_info.profit}\n")
