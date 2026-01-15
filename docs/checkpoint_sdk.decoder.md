checkpoint_sdk.decoder package
******************************


Submodules
==========


checkpoint_sdk.decoder.decoder module
=====================================

class checkpoint_sdk.decoder.decoder.Decoder(programs)

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


checkpoint_sdk.decoder.exceptions module
========================================

exception checkpoint_sdk.decoder.exceptions.NoElements

   Bases: "Exception"

exception checkpoint_sdk.decoder.exceptions.NoIDLMatch

   Bases: "Exception"

exception checkpoint_sdk.decoder.exceptions.TooManyElements

   Bases: "Exception"


Module contents
===============
