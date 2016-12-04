import os
import sys
import dpkt

from plugins import plugin_list
from impacket import ImpactDecoder

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

filename = raw_input("Input PCAP filename: ")

decoder = ImpactDecoder.EthDecoder()

for ts, pkt in dpkt.pcap.Reader(open(filename, 'r')):
    for plugin in plugin_list:
        plugin.handler(decoder.decode(pkt))
