import os
import sys
import dpkt

from impacket import ImpactDecoder

from plugins import plugin_list

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

decoder = ImpactDecoder.EthDecoder()

filename = raw_input("Input PCAP filename: ")

for _, raw_pkt in dpkt.pcap.Reader(open(filename, 'r')):
    pkt = decoder.decode(raw_pkt)
    for plugin in plugin_list:
        plugin.handler(pkt)
