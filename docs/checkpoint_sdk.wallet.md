checkpoint_sdk.wallet package
*****************************


Submodules
==========


checkpoint_sdk.wallet.exceptions module
=======================================

exception checkpoint_sdk.wallet.exceptions.InsufficientBalance

   Bases: "Exception"


checkpoint_sdk.wallet.wallet module
===================================

class checkpoint_sdk.wallet.wallet.TransferConfig(fixed_fee_lamports: int = 0, min_amount_lamports: int = 0, max_amount_lamports: int = 9223372036854775807, enabled: bool = True)

   Bases: "object"

class checkpoint_sdk.wallet.wallet.WalletManager(rpc_url: str = 'https://api.mainnet-beta.solana.com', base_wallet_keypair: Keypair | None = None)

   Bases: "object"

   airdrop(wallet_id: str, amount_sol: float = 1.0) -> str

   create_wallet() -> str

   estimate_transfer_fee(amount_sol: float, use_config: bool = False) -> float

   get_balance(wallet_id: str) -> int

   get_balance_sol(wallet_id: str) -> float

   get_network_info() -> Dict

   get_recent_blockhash() -> str

   get_transaction_history(wallet_id: str | None = None) -> list

   get_wallet_private_key(wallet_id: str) -> str

   get_wallet_public_key(wallet_id: str) -> str

   import_wallet_from_private_key(private_key_base58: str) -> str

   instant_transfer(from_wallet_id: str, to_wallet_id: str, amount_sol: float, use_config: bool = False, custom_config: TransferConfig | None = None) -> Dict

   set_transfer_config(fixed_fee_sol: float = 0.0, min_amount_sol: float = 0.0, max_amount_sol: float = inf, enabled: bool = True)

   transfer(from_wallet_id: str, to_wallet_id: str, amount_sol: float, use_config: bool = False, custom_config: TransferConfig | None = None) -> str


Module contents
===============
