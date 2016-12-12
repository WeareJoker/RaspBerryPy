from scapy.all import *

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from .plugins import plugin_list


def analysis(pcap_filename):
    for pkt in rdpcap(pcap_filename):
        for plugin in plugin_list:
            plugin.handler(pkt)


if __name__ == '__main__':
    analysis(input("PCAP: "))
