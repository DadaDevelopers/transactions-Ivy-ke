# Transaction Decoding Assignment

My work for decoding a raw Bitcoin transaction using the provided transaction hex.

## Files

* `manual-decode.md` — Task 1: manual transaction decoding
* `decoder.py` — Task 2: Python transaction decoder
* `output.txt` — output from running the decoder
* `README.md` — project notes

## About the Decoder

The Python script reads the transaction hex from beginning to end and separates it into the different transaction fields.

It handles:

* Transaction version
* SegWit marker and flag
* Inputs
* Outputs
* Witness data
* Locktime
* Bitcoin VarInts

The script supports both legacy and SegWit transactions.

The `read_varint()` function is used whenever the transaction contains a variable-length value, such as the number of inputs, outputs, or the length of a script.

For fields stored in little-endian format, Python's `int.from_bytes(..., 'little')` is used to get the correct value. The previous transaction hash is reversed when displayed because Bitcoin explorers normally show txids in the opposite byte order from how they are stored in the transaction.

## Running the Decoder

```bash
python3 decoder.py
```

The script uses the transaction hex stored in `tx_hex` and prints the decoded information as JSON.

To test another transaction, the value of `tx_hex` can be replaced with another raw transaction hex.

## Verification

I checked the Python output against my manual decoding from Task 1.

The first output was decoded as `500000` satoshis, which matched the expected value. The decoder also reported that all `222` bytes were consumed, confirming that the transaction was parsed completely.
