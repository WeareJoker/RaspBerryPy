from scapy.all import *

from plugins import plugin_list

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

filename = input("Input PCAP filename: ")


for pkt in rdpcap(filename):
    for plugin in plugin_list:
        plugin.handler(pkt)
