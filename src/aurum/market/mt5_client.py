import MetaTrader5 as mt5

from aurum.market.settings import MT5Settings


def connect(settings: MT5Settings) -> None:
    ok = mt5.initialize(
        login=settings.mt5_login,
        password=settings.mt5_password,
        server=settings.mt5_server,
    )
    if not ok:
        raise RuntimeError(f"MT5 initialize failed: {mt5.last_error()}")


def disconnect() -> None:
    mt5.shutdown()
