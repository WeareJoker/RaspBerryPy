from scapy.all import *
from analysis.plugins import plugin_list
from multiprocessing import Process


def packet_handler(pkt):
    for plugin in plugin_list:
        p = Process(target=plugin.handler, args=(pkt,))
        p.start()


def analysis_pcap(pcap_filename):
    for pkt in rdpcap(pcap_filename):
        packet_handler(pkt)


def analysis_sniff(interface):
    sniff(iface=interface, prn=packet_handler)


def migrate():
    for module in plugin_list:
        module.model.Base.metadata.create_all()
