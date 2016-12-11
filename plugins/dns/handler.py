from _socket import inet_ntoa

from dpkt.dns import DNS as p_DNS
from model import DNS
from database import Session
from utility import ether2data

session = Session()


def handler(pkt):
    dns = p_DNS(ether2data(pkt).get_packet())

    if len(dns.an) == 0:
        host = dns.qd[0].name
        ip = None
        session.add(DNS(host, ip))
    else:
        for ans in dns.an:
            host = ans.name
            try:
                ip = inet_ntoa(ans.ip)
            except AttributeError:
                ip = ans.cname
            session.add(DNS(host, ip))

    session.commit()
