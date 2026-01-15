checkpoint_sdk.transaction package
**********************************


Submodules
==========


checkpoint_sdk.transaction.exceptions module
============================================

exception checkpoint_sdk.transaction.exceptions.EncodingNotSupported

   Bases: "Exception"

exception checkpoint_sdk.transaction.exceptions.InvalidTransactionError

   Bases: "TransactionError"

exception checkpoint_sdk.transaction.exceptions.RPCConnectionError

   Bases: "TransactionError"

exception checkpoint_sdk.transaction.exceptions.TransactionError

   Bases: "Exception"

exception checkpoint_sdk.transaction.exceptions.TransactionNotFoundError

   Bases: "TransactionError"

exception checkpoint_sdk.transaction.exceptions.TransactionTimeoutError

   Bases: "TransactionError"


checkpoint_sdk.transaction.transaction module
=============================================

class checkpoint_sdk.transaction.transaction.TransactionConfig(encoding: checkpoint_sdk.transaction.transaction.TransactionEncoding = <TransactionEncoding.JSON_PARSED: 'jsonParsed'>, commitment: checkpoint_sdk.transaction.transaction.TransactionStatus = <TransactionStatus.CONFIRMED: 'confirmed'>, max_supported_transaction_version: int = 0, timeout: int = 30)

   Bases: "object"

   commitment: TransactionStatus = 'confirmed'

   encoding: TransactionEncoding = 'jsonParsed'

   max_supported_transaction_version: int = 0

   timeout: int = 30

class checkpoint_sdk.transaction.transaction.TransactionEncoding(*values)

   Bases: "str", "Enum"

   BASE58 = 'base58'

   BASE64 = 'base64'

   JSON_PARSED = 'jsonParsed'

class checkpoint_sdk.transaction.transaction.TransactionManager(rpc_url: str = 'https://api.mainnet-beta.solana.com', headers: Dict[str, str] | None = None, config: TransactionConfig | None = None)

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

class checkpoint_sdk.transaction.transaction.TransactionStatus(*values)

   Bases: "str", "Enum"

   CONFIRMED = 'confirmed'

   FINALIZED = 'finalized'

   PROCESSED = 'processed'


Module contents
===============
