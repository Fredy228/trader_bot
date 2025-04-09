import MetaTrader5 as mt5

def connect():
    print("Connecting...")

    connect = mt5.initialize()
    print("Connect: ", connect)

    if not connect:
        print("Error connecting :(")
        print(mt5.last_error())
        mt5.shutdown()
        exit()