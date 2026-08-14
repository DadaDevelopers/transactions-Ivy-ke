def read_varint(data, offset):
    first = data[offset]

    if first < 0xfd:
        return first, offset + 1
    elif first == 0xfd:
        return int.from_bytes(data[offset+1:offset+3], 'little'), offset + 3
    elif first == 0xfe:
        return int.from_bytes(data[offset+1:offset+5], 'little'), offset + 5
    else:
        return int.from_bytes(data[offset+1:offset+9], 'little'), offset + 9


def decode_transaction(hex_string):
    data = bytes.fromhex(hex_string)
    offset = 0
    result = {}

    version = int.from_bytes(data[offset:offset+4], 'little')
    result['version'] = version
    offset += 4

    is_segwit = False

    if data[offset] == 0x00 and data[offset+1] == 0x01:
        is_segwit = True
        result['marker'] = format(data[offset], '02x')
        result['flag'] = format(data[offset+1], '02x')
        offset += 2
    else:
        result['marker'] = None
        result['flag'] = None

    input_count, offset = read_varint(data, offset)
    result['input_count'] = input_count

    inputs = []

    for _ in range(input_count):
        txid = data[offset:offset+32][::-1].hex()
        offset += 32

        vout = int.from_bytes(data[offset:offset+4], 'little')
        offset += 4

        script_len, offset = read_varint(data, offset)
        script_sig = data[offset:offset+script_len].hex()
        offset += script_len

        sequence = data[offset:offset+4]
        offset += 4

        inputs.append({
            'txid': txid,
            'vout': vout,
            'script_length': script_len,
            'scriptSig': script_sig if script_sig else '(empty)',
            'sequence_hex': sequence.hex(),
            'sequence_value': int.from_bytes(sequence, 'little')
        })

    result['inputs'] = inputs

    output_count, offset = read_varint(data, offset)
    result['output_count'] = output_count

    outputs = []

    for _ in range(output_count):
        amount = int.from_bytes(data[offset:offset+8], 'little')
        offset += 8

        script_len, offset = read_varint(data, offset)
        script_pubkey = data[offset:offset+script_len].hex()
        offset += script_len

        outputs.append({
            'amount_satoshis': amount,
            'amount_btc': amount / 100_000_000,
            'script_length': script_len,
            'scriptPubKey': script_pubkey
        })

    result['outputs'] = outputs

    witness_data = []

    if is_segwit:
        for _ in range(input_count):
            item_count, offset = read_varint(data, offset)
            items = []

            for _ in range(item_count):
                item_len, offset = read_varint(data, offset)
                item = data[offset:offset+item_len].hex()
                offset += item_len
                items.append(item)

            witness_data.append(items)

    result['witness'] = witness_data

    result['locktime'] = int.from_bytes(data[offset:offset+4], 'little')
    offset += 4

    result['bytes_consumed'] = offset
    result['total_bytes'] = len(data)
    result['fully_parsed'] = offset == len(data)

    return result


if __name__ == "__main__":
    tx_hex = "0200000000010131811cd355c357e0e01437d9bcf690df824e9ff785012b6115dfae3d8e8b36c10100000000fdffffff0220a107000000000016001485d78eb795bd9c8a21afefc8b6fdaedf718368094c08100000000000160014840ab165c9c2555d4a31b9208ad806f89d2535e20247304402207bce86d430b58bb6b79e8c1bbecdf67a530eff3bc61581a1399e0b28a741c0ee0220303d5ce926c60bf15577f2e407f28a2ef8fe8453abd4048b716e97dbb1e3a85c01210260828bc77486a55e3bc6032ccbeda915d9494eda17b4a54dbe3b24506d40e4ff43030e00"

    decoded = decode_transaction(tx_hex)

    import json
    print(json.dumps(decoded, indent=2))
