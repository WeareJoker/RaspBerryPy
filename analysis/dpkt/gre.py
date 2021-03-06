# $Id: gre.py 75 2010-08-03 14:42:19Z jon.oberheide $
# -*- coding: utf-8 -*-
"""Generic Routing Encapsulation."""

import struct

from . import dpkt
from .decorators import deprecated

GRE_CP = 0x8000  # Checksum Present
GRE_RP = 0x4000  # Routing Present
GRE_KP = 0x2000  # Key Present
GRE_SP = 0x1000  # Sequence Present
GRE_SS = 0x0800  # Strict Source Route
GRE_AP = 0x0080  # Acknowledgment Present

GRE_opt_fields = (
    (GRE_CP | GRE_RP, 'sum', 'H'), (GRE_CP | GRE_RP, 'off', 'H'),
    (GRE_KP, 'key', 'I'), (GRE_SP, 'seq', 'I'), (GRE_AP, 'ack', 'I')
)


class GRE(dpkt.Packet):
    __hdr__ = (
        ('flags', 'H', 0),
        ('p', 'H', 0x0800),  # ETH_TYPE_IP
    )
    _protosw = {}
    sre = ()

    @property
    def v(self):
        return self.flags & 0x7

    @v.setter
    def v(self, v):
        self.flags = (self.flags & ~0x7) | (v & 0x7)

    @property
    def recur(self):
        return (self.flags >> 5) & 0x7

    @recur.setter
    def recur(self, v):
        self.flags = (self.flags & ~0xe0) | ((v & 0x7) << 5)

    # Deprecated methods, will be removed in the future
    # =================================================
    @deprecated('v')
    def get_v(self): return self.v

    @deprecated('v')
    def set_v(self, v): self.v = v

    @deprecated('recur')
    def get_recur(self): return self.recur

    @deprecated('recur')
    def set_recur(self, v): self.recur = v
    # =================================================

    class SRE(dpkt.Packet):
        __hdr__ = [
            ('family', 'H', 0),
            ('off', 'B', 0),
            ('len', 'B', 0)
        ]

        def unpack(self, buf):
            dpkt.Packet.unpack(self, buf)
            self.data = self.data[:self.len]

    def opt_fields_fmts(self):
        if self.v == 0:
            fields, fmts = [], []
            opt_fields = GRE_opt_fields
        else:
            fields, fmts = ['len', 'callid'], ['H', 'H']
            opt_fields = GRE_opt_fields[-2:]
        for flags, field, fmt in opt_fields:
            if self.flags & flags:
                fields.append(field)
                fmts.append(fmt)
        return fields, fmts

    def unpack(self, buf):
        dpkt.Packet.unpack(self, buf)
        fields, fmts = self.opt_fields_fmts()
        if fields:
            fmt = b''.join(fmts)
            fmtlen = struct.calcsize(fmt)
            vals = struct.unpack(fmt, self.data[:fmtlen])
            self.data = self.data[fmtlen:]
            self.__dict__.update(dict(list(zip(fields, vals))))
        if self.flags & GRE_RP:
            l = []
            while True:
                sre = self.SRE(self.data)
                self.data = self.data[len(sre):]
                l.append(sre)
                if not sre.len:
                    break
            self.sre = l
        self.data = ethernet.Ethernet._typesw[self.p](self.data)
        setattr(self, self.data.__class__.__name__.lower(), self.data)

    def __len__(self):
        opt_fmtlen = struct.calcsize(b''.join(self.opt_fields_fmts()[1]))
        return self.__hdr_len__ + opt_fmtlen + sum(map(len, self.sre)) + len(self.data)

    def __str__(self):
        return str(self.__bytes__())
    
    def __bytes__(self):
        fields, fmts = self.opt_fields_fmts()
        if fields:
            vals = []
            for f in fields:
                vals.append(getattr(self, f))
            opt_s = struct.pack(b''.join(fmts), *vals)
        else:
            opt_s = b''
        return self.pack_hdr() + opt_s + b''.join(map(bytes, self.sre)) + bytes(self.data)

# XXX - auto-load GRE dispatch table from Ethernet dispatch table
from . import ethernet

GRE._protosw.update(ethernet.Ethernet._typesw)
