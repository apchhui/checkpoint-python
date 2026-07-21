from .decoder.decoder import Decoder
from .transaction.transaction import TransactionManager

__all__ = [
    "Decoder",
    "TransactionManager",
    "WalletManager",
]


def __getattr__(name):
    # WalletManager is imported lazily so that a problem in the wallet module
    # (or one of its dependencies) can never break `from checkpoint_sdk import
    # Decoder` - which is the part of this package basically everyone uses.
    if name == "WalletManager":
        from .wallet.wallet import WalletManager

        return WalletManager
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
