# checkpoint-python

Solana SDK for:
- Real-time transaction decoding via Anchor IDL
- Program-agnostic decoding
- Batch RPC fetching
- Wallet utilities
- etc.

Wallet Manager is beta!!!

# Installation with pip

```bash
pip install checkpoint-sdk
```

# Example usage:
```python
from checkpoint_sdk import Decoder
# from checkpoint_sdk.decoder import Decoder  # also works

PROGRAM_ID = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"

decoder = Decoder([PROGRAM_ID])

result = decoder.decode("vdt/007m", PROGRAM_ID)  # Example b64 data

print(result)
```

If the built-in IDL auto-fetch 403s (it hits an undocumented Solscan
endpoint, which blocks non-browser requests fairly often), pass your own:

```python
import json

idl = json.load(open("pump.json"))  # from the program's own public source repo
decoder = Decoder([PROGRAM_ID], idls={PROGRAM_ID: idl})
```

# 0.2.0 changes

Fixed, without changing the public shape of anything except `WalletManager`:

- **`import checkpoint_sdk` no longer crashes on a fresh install.**
  `checkpoint_sdk/__init__.py` unconditionally imported `WalletManager`,
  which imported `solana.rpc.api.Client` - a module solana-py removed in
  favor of the async-only client. `WalletManager` is now imported lazily, so
  a problem in the wallet module can't break `Decoder`/`TransactionManager`.
- **`from checkpoint_sdk.decoder import Decoder` (this README's own example)
  now actually works.** `decoder/__init__.py` (and `transaction/__init__.py`,
  `wallet/__init__.py`) were empty.
- **`Decoder.IDLs` is an instance attribute now, not a class attribute.**
  Previously every `Decoder` you created in the same process shared (and
  kept appending to) the same list.
- **`Decoder(programs, idls={...})`** - pass pre-loaded IDLs directly instead
  of subclassing to override `_fetch_idl()`. See the Solscan 403 note above.
- **`extract_program_data()` / `extract_all_program_data()` now track the
  actual invoke/success call stack** instead of assuming a `Program data:`
  line always precedes the next invoke of the same program - which breaks
  on transactions with nested self-CPI event logging. Also fixed an
  off-by-one that silently dropped a data line if it was the very last log
  line.

**Breaking change:** `WalletManager`'s methods are `async def` now
(`get_balance`, `transfer`, `instant_transfer`, `airdrop`,
`get_recent_blockhash`, `estimate_transfer_fee`, `get_network_info` all need
`await`; there's also a new `await wallet.close()`). This wasn't optional -
the synchronous `solana.rpc.api.Client` it depended on no longer exists in
current solana-py, so there was no working synchronous behavior left to
preserve. Verified end-to-end against Solana devnet (client construction,
wallet creation, network info, balance checks, and the insufficient-balance
error path); the airdrop-then-send round trip specifically couldn't be
re-confirmed live in one sitting because the public devnet faucet was
rate-limited at the time - transaction construction/signing itself uses the
same `MessageV0` + `VersionedTransaction` pattern already verified in the
decoder/transaction paths.

# Documentation:
(https://github.com/apchhui/checkpoint-python/tree/main/docs)
