# Task 1: Manual Transaction Decode

**Transaction Hex:**

```text
0200000000010131811cd355c357e0e01437d9bcf690df824e9ff785012b6115dfae3d8e8b36c10100000000fdffffff0220a107000000000016001485d78eb795bd9c8a21afefc8b6fdaedf718368094c08100000000000160014840ab165c9c2555d4a31b9208ad806f89d2535e20247304402207bce86d430b58bb6b79e8c1bbecdf67a530eff3bc61581a1399e0b28a741c0ee0220303d5ce926c60bf15577f2e407f28a2ef8fe8453abd4048b716e97dbb1e3a85c01210260828bc77486a55e3bc6032ccbeda915d9494eda17b4a54dbe3b24506d40e4ff43030e00
```

**Transaction:**
https://mempool.space/tx/04f487fe9754a925c2e96492afeab47e7c839d0582eef80b3ecc9ca3afa05842

## How I Decoded It

I decoded the transaction by going through the hexadecimal data from the beginning and reading each field in the order it appears. For every field, I kept track of how many bytes it used before moving to the next one.

I also wrote a decoder for Task 2 and used it to check my manual work. The field sizes and values matched, and there were no bytes left over at the end. The first output was also `500,000` satoshis (`0.005 BTC`), which matched the worked example provided in the assignment.

A few things are important to keep in mind when reading the transaction:

* Bitcoin uses **little-endian byte order** for many multi-byte values, including the version, output amounts, sequence number, and locktime. This means the bytes have to be read in reverse order when converting them into normal numbers.
* Transaction hashes and previous transaction hashes are stored in little-endian form internally, but they are normally displayed in the opposite order by wallets and block explorers. I therefore reversed the hash bytes when displaying them.
* Bitcoin uses **VarInt encoding** for things such as input counts, output counts, and script or witness lengths. Small values can be represented by a single byte, while larger values use a prefix followed by additional bytes.
* The `00 01` immediately after the version identifies this as a **SegWit transaction**. The `00` is the SegWit marker and the `01` is the flag.

---

## Decoded Fields

```text
=== Manual Transaction Decode ===

Version: 2

Marker: 00
Flag: 01

Input Count: 1

Input #1:
  Previous TX Hash: c1368b8e3daedf15612b0185f79f4e82df90f6bcd93714e0e057c355d31c8131
  Previous Output Index: 1
  Script Length: 0
  ScriptSig: (empty)
  Sequence: fdffffff  (0xfffffffd — RBF opt-in)

Output Count: 2

Output #1:
  Amount (satoshis): 500000  (0.005 BTC)
  Script Length: 22
  ScriptPubKey: 001485d78eb795bd9c8a21afefc8b6fdaedf7183680  (P2WPKH)

Output #2:
  Amount (satoshis): 1050700  (0.010507 BTC)
  Script Length: 22
  ScriptPubKey: 0014840ab165c9c2555d4a31b9208ad806f89d2535e  (P2WPKH)

Witness Data:
  Input #1 has 2 witness items:

    1. Signature:
       304402207bce86d430b58bb6b79e8c1bbecdf67a530eff3bc61581a1399e0b28a741c0ee0220303d5ce926c60bf15577f2e407f28a2ef8fe8453abd4048b716e97dbb1e3a85c01

    2. Public Key:
       0260828bc77486a55e3bc6032ccbeda915d9494eda17b4a54dbe3b24506d40e4ff

Locktime: 918339
```

---

## Explanation of the Important Fields

### Empty ScriptSig

The `scriptSig` is empty because this input is spending a native SegWit (P2WPKH) output.

In a traditional Bitcoin transaction, the signature and public key would normally be included in the `scriptSig`. With SegWit, this information is moved into the **witness** section instead.

That is why the transaction has an empty `scriptSig` but still contains a signature and public key later in the transaction.

### Sequence: `fdffffff`

The sequence bytes are `fdffffff`. Because Bitcoin uses little-endian encoding, this represents:

```text
0xfffffffd
```

This value is below `0xfffffffe`, so it indicates that the transaction signals **Replace-By-Fee (RBF)** under BIP125.

In simple terms, this means the transaction can potentially be replaced with another version paying a higher fee before it is confirmed.

The sequence value also does not activate a relative timelock in this case.

### ScriptPubKey: `0014...`

Both outputs start with:

```text
0014
```

This represents the standard native SegWit **P2WPKH** script.

The `00` represents the witness version, while `14` indicates that the following data is 20 bytes long. The 20-byte value is the public-key hash used by P2WPKH.

This is the same native SegWit format represented by **Bech32 addresses**, which I looked at in the previous assignment.

### Locktime: `918339`

The final four bytes contain the transaction's locktime, which decodes to:

```text
918339
```

Bitcoin uses the value of locktime to determine whether it represents a block height or a Unix timestamp. Values below `500,000,000` are interpreted as block heights.

Therefore, `918339` represents **block height 918,339** rather than a specific date and time.

This means the transaction's locktime is based on the blockchain reaching that block height.

## Summary

By manually decoding the transaction, I was able to identify the version, SegWit marker and flag, input, outputs, witness data, and locktime.

The transaction contains **one input and two outputs**, and both outputs use the native SegWit P2WPKH format. The input has an empty `scriptSig` because its signature and public key are stored in the witness section. The sequence value also shows that RBF is enabled.

Going through the transaction byte-by-byte helped me understand how the hexadecimal representation is structured and how the different fields fit together to form a complete Bitcoin transaction.
