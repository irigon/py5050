# Self-Delimiting Numeric Values (SDVNs) -- https://tools.ietf.org/html/rfc5050

import struct

# given a big int, return an array of encoded bytes
def encode(data):
    encoded = b''
    hbit = 0
    while True:
        byte = hbit | (data & 0x7f)
        hbit = 1 << 7                       # just first byte with hbit==0
        encoded = struct.pack('B', byte) + encoded
        data = data >> 7          # consume next 7 bits
        if data == 0:
            break
    return encoded

# given an array of bytes, return an int
def decode(data, offset = 0):
    decoded = 0
    n = offset
    while data[n] & 0x80:
        decoded <<=7
        decoded |= (data[n] & 0x7f)
        n += 1
    decoded |= data[n]
    return decoded, (n+1) - offset # n+1 - offset == len

def decode_header(h):
    assert h[:4] == b'dtn!', 'header should start with "dtn!"'
    assert len(h) > 8, 'header too short'
    result = {
        "version": h[4],
        "flags": h[5],
        "keepalive": struct.unpack("!h", h[6:8])[0]
    }

    eid_len, eid_len_size = decode(h, 8)
    assert len(h) == 8 + eid_len_size + eid_len, "header length does not match"
    result["eid"] = h[8 + eid_len_size:].decode("ascii")
    return result

