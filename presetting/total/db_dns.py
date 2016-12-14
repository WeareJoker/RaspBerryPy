import os
import sys

from scapy.all import *
from db import *

session = Session()


def dns_handler(data):
    if data.haslayer("DNS"):
        dns_packet = data.payload.payload.payload
    else:
        return

    for cnt in range(dns_packet.ancount):
        if dns_packet.an[cnt].type != 6:
            session.add(
                DNS(dns_packet.an[cnt].rrname,
                    str(dns_packet.an[cnt].ttl),
                    str(dns_packet.an[cnt].type),
                    dns_packet.an[cnt].rdata))
            session.commit()

    for cnt in range(dns_packet.nscount):
        if dns_packet.ns[cnt].type != 6:
            session.add(
                DNS(dns_packet.ns[cnt].rrname,
                    str(dns_packet.ns[cnt].ttl),
                    str(dns_packet.ns[cnt].type),
                    dns_packet.ns[cnt].rdata))
            session.commit()

    for cnt in range(dns_packet.arcount):
        if dns_packet.ar[cnt].type != 6:
            session.add(
                DNS(dns_packet.ar[cnt].rrname,
                    str(dns_packet.ar[cnt].ttl),
                    str(dns_packet.ar[cnt].type),
                    dns_packet.ar[cnt].rdata))
            session.commit()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Input Condition 'interface' or 'pcap'")
        sys.exit()
    else:
        if sys.argv[1] == "pcap":
            filename = input("Input File Name : ")
            now_path = os.path.dirname(os.path.abspath(__file__))
            pcap_path = os.path.join(now_path, filename)
            pcap = rdpcap(pcap_path)
            for packet in pcap:
                dns_handler(packet)
        else:
            sniff(iface=sys.argv[1], prn=dns_handler, filter="udp port 53")
        