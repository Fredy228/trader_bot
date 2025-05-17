import MetaTrader5 as mt5
from services.logger import logger


def connect():
    logger.info("Підключення до MetaTrader 5...")
    print("\nПідключення до MetaTrader 5...\n")

    connect = mt5.initialize()
    logger.info(f"Статус підключення: {connect}")
    print(f"Статус підключення: {connect}")

    if not connect:
        logger.error("Помилка підключення :(")
        print("Помилка підключення :(")
        logger.error(mt5.last_error())
        mt5.shutdown()
        exit()
