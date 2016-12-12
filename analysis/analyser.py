from scapy.all import *
from analysis.plugins import plugin_list


def analysis(pcap_filename):
    for pkt in rdpcap(pcap_filename):
        for plugin in plugin_list:
            plugin.handler(pkt)


def migrate():
    for module in plugin_list:
        module.model.Base.metadata.create_all()
