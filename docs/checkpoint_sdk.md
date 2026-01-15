checkpoint_sdk package
**********************


Subpackages
===========

* checkpoint_sdk.decoder package

  * Submodules

  * checkpoint_sdk.decoder.decoder module

    * "Decoder"

      * "Decoder.IDLs"

      * "Decoder.MAX"

      * "Decoder.batch_decode()"

      * "Decoder.decode()"

      * "Decoder.decode_on_demand()"

      * "Decoder.extract_all_program_data()"

      * "Decoder.extract_program_data()"

  * checkpoint_sdk.decoder.exceptions module

    * "NoElements"

    * "NoIDLMatch"

    * "TooManyElements"

  * Module contents

* checkpoint_sdk.transaction package

  * Submodules

  * checkpoint_sdk.transaction.exceptions module

    * "EncodingNotSupported"

    * "InvalidTransactionError"

    * "RPCConnectionError"

    * "TransactionError"

    * "TransactionNotFoundError"

    * "TransactionTimeoutError"

  * checkpoint_sdk.transaction.transaction module

    * "TransactionConfig"

      * "TransactionConfig.commitment"

      * "TransactionConfig.encoding"

      * "TransactionConfig.max_supported_transaction_version"

      * "TransactionConfig.timeout"

    * "TransactionEncoding"

      * "TransactionEncoding.BASE58"

      * "TransactionEncoding.BASE64"

      * "TransactionEncoding.JSON_PARSED"

    * "TransactionManager"

      * "TransactionManager.close()"

      * "TransactionManager.confirm_transaction()"

      * "TransactionManager.get_latest_blockhash()"

      * "TransactionManager.get_program_accounts()"

      * "TransactionManager.get_signatures_for_address()"

      * "TransactionManager.get_transaction()"

      * "TransactionManager.get_transaction_batch()"

      * "TransactionManager.get_transaction_cost()"

      * "TransactionManager.get_transaction_history()"

      * "TransactionManager.parse_transaction_data()"

      * "TransactionManager.simulate_transaction()"

    * "TransactionStatus"

      * "TransactionStatus.CONFIRMED"

      * "TransactionStatus.FINALIZED"

      * "TransactionStatus.PROCESSED"

  * Module contents

* checkpoint_sdk.wallet package

  * Submodules

  * checkpoint_sdk.wallet.exceptions module

    * "InsufficientBalance"

  * checkpoint_sdk.wallet.wallet module

    * "TransferConfig"

    * "WalletManager"

      * "WalletManager.airdrop()"

      * "WalletManager.create_wallet()"

      * "WalletManager.estimate_transfer_fee()"

      * "WalletManager.get_balance()"

      * "WalletManager.get_balance_sol()"

      * "WalletManager.get_network_info()"

      * "WalletManager.get_recent_blockhash()"

      * "WalletManager.get_transaction_history()"

      * "WalletManager.get_wallet_private_key()"

      * "WalletManager.get_wallet_public_key()"

      * "WalletManager.import_wallet_from_private_key()"

      * "WalletManager.instant_transfer()"

      * "WalletManager.set_transfer_config()"

      * "WalletManager.transfer()"

  * Module contents


Module contents
===============

class checkpoint_sdk.Decoder(programs)

   Bases: "object"

   IDLs = []

   MAX = 6

   batch_decode(extract_all_program_data_result: list, program_address: str) -> List[dict] | None

   decode(base64_str: str, program_address: str)

      Decodes input *Program data:* base64 string by program IDL

   decode_on_demand(tx, program_id)

      Automatically extracts first entry *Program data:* of set
      program address and returns decoded data

   extract_all_program_data(tx)

      Extracts all *Program data:* strings from tx, so you can use it
      to *unsafe* parse all your strings using batch_decode()

   extract_program_data(tx: Dict, program_address: str) -> str | None

      This function only works in some cases!!! Be care using it, not
      always we can find correct str, so in most cases you need to
      find base64 data at your own

class checkpoint_sdk.TransactionManager(rpc_url: str = 'https://api.mainnet-beta.solana.com', headers: Dict[str, str] | None = None, config: TransactionConfig | None = None)

   Bases: "object"

   close()

   confirm_transaction(signature: str, commitment: str | None = None, timeout: int = 30, poll_interval: int = 1) -> bool

   get_latest_blockhash(commitment: str | None = None) -> Dict[str, Any]

   get_program_accounts(program_id: str, encoding: str | None = None, commitment: str | None = None) -> Dict[str, Any]

   get_signatures_for_address(address: str, limit: int = 1000, before: str | None = None, until: str | None = None, commitment: str | None = None) -> Dict[str, Any]

   get_transaction(signature: str, encoding: str | None = None, commitment: str | None = None) -> Dict[str, Any]

   get_transaction_batch(signatures: List[str], encoding: str | None = None, commitment: str | None = None) -> List[Dict[str, Any]]

   get_transaction_cost(transaction_data: str) -> Dict[str, Any]

   get_transaction_history(address: str, limit: int = 10, encoding: str | None = None) -> List[Dict[str, Any]]

   parse_transaction_data(transaction_data: Dict[str, Any], format_output: bool = False) -> Dict[str, Any] | str

   simulate_transaction(transaction_data: str, commitment: str | None = None) -> Dict[str, Any]

class checkpoint_sdk.WalletManager(rpc_url: str = 'https://api.mainnet-beta.solana.com', base_wallet_keypair: Keypair | None = None)

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
