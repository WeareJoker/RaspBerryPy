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

    host_dict = dict()

    if len(dns.an) != 0:
        for ans in dns.an:
            host = ans.name
            try:
                ip = inet_ntoa(ans.ip)
            except AttributeError:
                ip = ans.cname

            host_dict[host] = ip

    for host in host_dict:
        try:
            session.add(DNSHost(host, host_dict[host]))
        except ValueError:
            continue

    session.commit()
