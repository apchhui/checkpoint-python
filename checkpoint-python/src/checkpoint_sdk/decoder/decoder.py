### --!-- --!-- --!-- better not to use python in Solana high performance production apps --!-- --!-- --!-- ###
import re
import requests
from typing import Optional, Dict, Any, Tuple, List
from checkpoint_sdk.decoder.exceptions import TooManyElements, NoElements
import base64
import struct

_INVOKE_RE = re.compile(r"^Program (\w+) invoke \[(\d+)\]$")
_RESULT_RE = re.compile(r"^Program (\w+) (success|failed)")

class Decoder:
    MAX = 6

    def __init__(self, programs, idls: Optional[Dict[str, Dict[str, Any]]] = None):
        """
        programs: program addresses to decode events for.
        idls: optional {program_address: idl_dict} of pre-loaded IDLs. Any
            program_address found here skips the live fetch entirely - useful
            because the built-in fetch hits an undocumented Solscan endpoint
            that returns 403 for non-browser requests fairly often. Fetch
            your own IDL (e.g. from the program's public source repo, or by
            reading its on-chain IDL account) and pass it here instead of
            relying on that endpoint.
        """
        # IDLs used to be a class attribute here, which meant every Decoder
        # instance in a process shared (and kept appending to) the same list.
        # It's an instance attribute now.
        self.IDLs = []

        programs_count = len(programs)

        if programs_count > self.MAX:
            raise TooManyElements(
                f"Too many programs input! Max programs supported: {self.MAX} | Current input: {programs_count}"
            )
        elif programs_count == 0:
            raise NoElements(
                f"No programs on input! Expected MIN: 1 | MAX: {self.MAX} elements array"
            )

        idls = idls or {}
        for program_address in programs:
            idl = idls.get(program_address) or self._fetch_idl(program_address)
            self.IDLs.append(idl)
    
    def _find_idl(self, program_address: str):
        for idl in self.IDLs:
            idl_address = idl.get("address")
            if idl_address and idl_address == program_address:
                return idl
    
    def decode(self, base64_str: str, program_address: str):
        """
        Decodes input `Program data:` base64 string by program IDL
        """
        if not isinstance(base64_str, str): raise ValueError(f"Base 64 must be typeof string! Current type: {type(base64_str)} | decode()")
        def normalize_b64(s: str) -> str:
            s = s.strip().split()[-1]
            return s + "=" * (-len(s) % 4)

        idl = self._find_idl(program_address)
        if not idl:
            raise ValueError(f"IDL not found for program: {program_address}")
            
        events = idl.get("events", [])

        b64_clean = normalize_b64(base64_str)
        base64_raw = base64.b64decode(b64_clean)
        discriminator = list(base64_raw[:8])

        for event in events:
            if event.get("discriminator") == discriminator:
                name = event.get("name")
                for _type in idl.get("types", []):
                    if _type.get("name") == name:
                        offset = 8
                        result = {}
                        if "type" in _type and "fields" in _type["type"]:
                            for arg in _type["type"]["fields"]:
                                val, offset = self._read_type(arg["type"], base64_raw, offset, idl)
                                result[arg["name"]] = val
                        return result
        return None

    def _read_primitive(self, t: str, data: bytes, offset: int) -> Tuple[Any, int]:
        if t == "bool":
            return data[offset] == 1, offset + 1

        if t == "u8":
            return data[offset], offset + 1
        if t == "i8":
            return struct.unpack_from("<b", data, offset)[0], offset + 1

        if t == "u16":
            return struct.unpack_from("<H", data, offset)[0], offset + 2
        if t == "i16":
            return struct.unpack_from("<h", data, offset)[0], offset + 2

        if t == "u32":
            return struct.unpack_from("<I", data, offset)[0], offset + 4
        if t == "i32":
            return struct.unpack_from("<i", data, offset)[0], offset + 4

        if t == "u64":
            return struct.unpack_from("<Q", data, offset)[0], offset + 8
        if t == "i64":
            return struct.unpack_from("<q", data, offset)[0], offset + 8

        if t == "u128":
            lo, hi = struct.unpack_from("<QQ", data, offset)
            return (hi << 64) | lo, offset + 16

        if t == "i128":
            lo, hi = struct.unpack_from("<QQ", data, offset)
            val = (hi << 64) | lo
            if hi & (1 << 63):
                val -= 1 << 128
            return val, offset + 16

        if t == "pubkey":
            pubkey_bytes = data[offset:offset+32]
            return self._bytes_to_base58(pubkey_bytes), offset + 32

        raise ValueError(f"Unknown primitive type: {t}")

    def _bytes_to_base58(self, data: bytes) -> str:
        alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        n = int.from_bytes(data, 'big')
        result = ''
        while n > 0:
            n, remainder = divmod(n, 58)
            result = alphabet[remainder] + result
        
        leading_zeros = 0
        for byte in data:
            if byte == 0:
                leading_zeros += 1
            else:
                break
        return '1' * leading_zeros + result

    def _read_vec(self, inner, data, offset, idl):
        length, offset = self._read_primitive("u32", data, offset)
        items = []

        for _ in range(length):
            val, offset = self._read_type(inner, data, offset, idl)
            items.append(val)

        return items, offset

    def _read_string(self, data, offset):
        length, offset = self._read_primitive("u32", data, offset)
        s = data[offset:offset+length].decode("utf-8")
        return s, offset + length

    def _read_bytes(self, data, offset):
        length, offset = self._read_primitive("u32", data, offset)
        return data[offset:offset+length], offset + length

    def _read_defined(self, name: str, data: bytes, offset: int, idl):
        type_def = None
        for t in idl.get("types", []):
            if t.get("name") == name:
                type_def = t
                break
        
        # if not type_def:
        #     raise ValueError(f"Type definition not found: {name}")

        kind = type_def["type"]["kind"]

        if kind == "struct":
            result = {}
            for field in type_def["type"]["fields"]:
                val, offset = self._read_type(field["type"], data, offset, idl)
                result[field["name"]] = val
            return result, offset

        if kind == "enum":
            discr, offset = self._read_primitive("u8", data, offset)
            if discr >= len(type_def["type"]["variants"]):
                raise ValueError(f"Invalid discriminator: {discr}")
                
            variant = type_def["type"]["variants"][discr]

            if "fields" not in variant:
                return variant["name"], offset

            if isinstance(variant["fields"], list):
                values = []
                for f in variant["fields"]:
                    if isinstance(f, dict):
                        val, offset = self._read_type(f.get("type", f), data, offset, idl)
                    else:
                        val, offset = self._read_type(f, data, offset, idl)
                    values.append(val)
                return {variant["name"]: values}, offset
            else:
                obj = {}
                for f in variant["fields"]:
                    val, offset = self._read_type(f["type"], data, offset, idl)
                    obj[f["name"]] = val
                return {variant["name"]: obj}, offset

    def _read_type(self, t, data: bytes, offset: int, idl):
        if isinstance(t, str):
            if t == "string":
                return self._read_string(data, offset)
            if t == "bytes":
                return self._read_bytes(data, offset)
            return self._read_primitive(t, data, offset)

        if isinstance(t, dict):

            if t.get("kind") == "struct":
                result = {}
                for field in t.get("fields", []):
                    val, offset = self._read_type(field["type"], data, offset, idl)
                    result[field["name"]] = val
                return result, offset

            if t.get("kind") == "enum":
                discr, offset = self._read_primitive("u8", data, offset)
                variant = t["variants"][discr]

                if "fields" not in variant:
                    return variant["name"], offset

                values = {}
                for f in variant.get("fields", []):
                    val, offset = self._read_type(f["type"], data, offset, idl)
                    values[f["name"]] = val

                return {variant["name"]: values}, offset

            if "option" in t:
                flag, offset = self._read_primitive("u8", data, offset)
                if flag == 0:
                    return None, offset
                return self._read_type(t["option"], data, offset, idl)

            if "vec" in t:
                return self._read_vec(t["vec"], data, offset, idl)

            if "array" in t:
                inner, size = t["array"]
                arr = []
                for _ in range(size):
                    val, offset = self._read_type(inner, data, offset, idl)
                    arr.append(val)
                return arr, offset

            if "defined" in t:
                return self._read_defined(t["defined"], data, offset, idl)

        raise ValueError(f"Unknown IDL type: {t}")

    def _attribute_program_data(self, logs: List[str]) -> List[Tuple[Optional[str], str]]:
        """
        Walk the logs' actual invoke/success call stack and return
        (program_id, base64_data) for every `Program data:` line, attributed
        to whichever program was really executing when it was logged.

        This replaces a heuristic that assumed a `Program data:` line always
        precedes the *next* invoke of the same program - true often enough to
        look right, but wrong on transactions with nested self-CPI event
        logging, where a different program's data line can end up immediately
        before your target program's invoke line.
        """
        stack: List[str] = []
        result: List[Tuple[Optional[str], str]] = []

        for line in logs:
            if not isinstance(line, str):
                continue

            m = _INVOKE_RE.match(line)
            if m:
                stack.append(m.group(1))
                continue

            m = _RESULT_RE.match(line)
            if m and stack and stack[-1] == m.group(1):
                stack.pop()
                continue

            if line.startswith("Program data:"):
                current = stack[-1] if stack else None
                result.append((current, line.replace("Program data:", "").strip()))

        return result

    def extract_program_data(self, tx: Dict, program_address: str) -> Optional[str]:
        """
        Finds the first `Program data:` log line actually emitted while
        `program_address` was executing, using the real invoke/success call
        stack rather than assuming line order.
        """
        params = tx.get("params")
        if not params:
            return None

        results = params.get("result")
        if not results:
            return None

        value = results.get("value")
        if not value:
            return None

        logs = value.get("logs")
        if not isinstance(logs, list):
            return None

        for prog, data in self._attribute_program_data(logs):
            if prog == program_address:
                return data

        return None

    def decode_on_demand(self, tx, program_id):
        """
        Automatically extracts first entry `Program data:` of set program address and returns decoded data
        """
        data = self.extract_program_data(tx, program_id)
        return self.decode(data, program_id) if data else None

    def extract_all_program_data(self, tx):
        """
        Extracts all `Program data:` strings from tx, so you can use it to `unsafe` parse all your strings using batch_decode()
        """
        params = tx.get("params")
        if not params:
            return None

        results = params.get("result")
        if not results:
            return None

        value = results.get("value")
        if not value:
            return None

        logs = value.get("logs")
        if not isinstance(logs, list):
            return None

        # (previously `range(len(logs) - 1)`, which silently dropped a
        # `Program data:` line if it happened to be the very last log line)
        return [data for _prog, data in self._attribute_program_data(logs)]

    def batch_decode(self, extract_all_program_data_result: list, program_address: str) -> Optional[List[dict]]:
        results = {}
        for data in extract_all_program_data_result:
            results[data[:10]] = self.decode(data, program_address)
        return results

    def _fetch_idl(self, program_address: str) -> Optional[Dict[str, Any]]:
        url = f"https://api-v2.solscan.io/v2/account/anchor_idl?address={program_address}"

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0",
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://solscan.io",
            "Referer": "https://solscan.io/",
        }

        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=30
            )

            response.raise_for_status()
            data = response.json()

            if data.get("success"):
                return data.get("data")

            return None

        except Exception as e:
            raise Exception(f"Error fetching IDL for {program_address}: {e}")