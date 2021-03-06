# $Id: stun.py 47 2008-05-27 02:10:00Z jon.oberheide $
# -*- coding: utf-8 -*-
"""Simple Traversal of UDP through NAT."""

import struct

from . import dpkt

# STUN - RFC 3489
# http://tools.ietf.org/html/rfc3489
# Each packet has a 20 byte header followed by 0 or more attribute TLVs.

# Message Types
BINDING_REQUEST = 0x0001
BINDING_RESPONSE = 0x0101
BINDING_ERROR_RESPONSE = 0x0111
SHARED_SECRET_REQUEST = 0x0002
SHARED_SECRET_RESPONSE = 0x0102
SHARED_SECRET_ERROR_RESPONSE = 0x0112

# Message Attributes
MAPPED_ADDRESS = 0x0001
RESPONSE_ADDRESS = 0x0002
CHANGE_REQUEST = 0x0003
SOURCE_ADDRESS = 0x0004
CHANGED_ADDRESS = 0x0005
USERNAME = 0x0006
PASSWORD = 0x0007
MESSAGE_INTEGRITY = 0x0008
ERROR_CODE = 0x0009
UNKNOWN_ATTRIBUTES = 0x000a
REFLECTED_FROM = 0x000b


class STUN(dpkt.Packet):
    __hdr__ = (
        ('type', 'H', 0),
        ('len', 'H', 0),
        ('xid', '16s', 0)
    )


def tlv(buf):
    n = 4
    t, l = struct.unpack('>HH', buf[:n])
    v = buf[n:n + l]
    buf = buf[n + l:]
    return t, l, v, buf


def parse_attrs(buf):
    """Parse STUN.data buffer into a list of (attribute, data) tuples."""
    attrs = []
    while buf:
        t, _, v, buf = tlv(buf)
        attrs.append((t, v))
    return attrs


def test_stun_response():
    s = b'\x01\x01\x00\x0c\x21\x12\xa4\x42\x53\x4f\x70\x43\x69\x69\x35\x4a\x66\x63\x31\x7a\x00\x01\x00\x08\x00\x01\x11\x22\x33\x44\x55\x66'
    m = STUN(s)
    assert m.type == BINDING_RESPONSE
    assert m.len == 12

    attrs = parse_attrs(m.data)
    assert attrs == [(MAPPED_ADDRESS, b'\x00\x01\x11\x22\x33\x44\x55\x66'), ]


if __name__ == '__main__':
    test_stun_response()

    print('Tests Successful...')
