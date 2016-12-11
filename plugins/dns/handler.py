from _socket import inet_ntoa

from dpkt.dns import DNS
from dpkt.dpkt import UnpackError

from database import Session
from model import DNSHost
from utility import ether2data

session = Session()


def handler(pkt):
    try:
        dns = DNS(ether2data(pkt).get_packet())
    except (UnpackError, AttributeError):
        return

    if len(dns.an) != 0:
        for ans in dns.an:
            host = ans.name
            try:
                ip = inet_ntoa(ans.ip)
            except AttributeError:
                ip = ans.cname

            try:
                session.add(DNSHost(host, ip))
            except ValueError:
                continue

    session.commit()
