import os
import sys

import dpkt
from scapy.layers.l2 import Ether

from plugins import plugin_list

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

filename = raw_input("Input PCAP filename: ")


for ts, pkt in dpkt.pcap.Reader(open(filename, 'r')):
    packet = Ether(pkt)
    for plugin in plugin_list:
        plugin.handler(packet)
