from _socket import inet_ntoa

from dpkt.dns import DNS
from model import DNSHost
from database import Session
from utility import ether2data

session = Session()


def handler(pkt):
    dns = DNS(ether2data(pkt).get_packet())

    if len(dns.an) == 0:
        host = dns.qd[0].name
        ip = None
        session.add(DNSHost(host, ip))
    else:
        for ans in dns.an:
            host = ans.name
            try:
                ip = inet_ntoa(ans.ip)
            except AttributeError:
                ip = ans.cname
            session.add(DNSHost(host, ip))

    session.commit()
