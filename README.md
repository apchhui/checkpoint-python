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
from checkpoint_sdk.decoder import Decoder

PROGRAM_ID = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"

decoder = Decoder([PROGRAM_ID])

result = decoder.decode("vdt/007m", PROGRAM_ID)  # Example b64 data

print(result)
```

# Documentation:
(https://github.com/apchhui/checkpoint-python/tree/main/docs)
