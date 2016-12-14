from db import *

import re
import os
import sqlite3
import requests
import sys
from scapy.all import *
from multiprocessing import Process

import naver_mail_list_sniffer
import kakao_sniffer
import cookie_collector
import db_dns

SIZE_LIST = []
time_duplicate = {}

session = Session()

def plugin_handler(packet):
	if packet.haslayer("TCP"):
		naver_mail_list_sniffer.cookie_sniff(packet, SIZE_LIST, time_duplicate)
		kakao_sniffer.http_header(packet)
		cookie_collector.cookie_collect(packet)
	elif packet.haslayer("DNS"):
		db_dns.dns_handler(packet)
	else:
		return




def packet_handler(packet):
	plugin_proc = Process(target=plugin_handler, args=(packet,))
	plugin_proc.start()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Input Condition 'interface' or 'pcap'")
        print("USAGE : %s Condition - interface or pcap" % sys.argv[0])
        sys.exit()

    else:
        if sys.argv[1] == "pcap":
            filename = input("Input File Name : ")
            now_path = os.path.dirname(os.path.abspath(__file__))
            pcap_path = os.path.join(now_path, filename)
            pcap = rdpcap(pcap_path)
            for packet in pcap:
            	plugin_proc = Process(target=plugin_handler, args=(packet,))
            	plugin_proc.start()
        else:
            sniff(iface=sys.argv[1], prn=packet_handler, filter="tcp port 80 or udp port 53") ## start sniffing
        
