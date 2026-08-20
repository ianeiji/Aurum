import MetaTrader5 as mt5

from aurum.market.mt5_client import connect, disconnect
from aurum.market.settings import MT5Settings


def main() -> None:
    settings = MT5Settings()
    connect(settings)
    try:
        info = mt5.account_info()
        if info is None:
            raise RuntimeError(f"account_info failed: {mt5.last_error()}")
        print(f"server={info.company}/{info.server}")
        print(f"currency={info.currency}")
        print(f"balance={info.balance}")
        print(f"equity={info.equity}")
    finally:
        disconnect()


if __name__ == "__main__":
    main()
