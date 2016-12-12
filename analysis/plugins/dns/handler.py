from analysis.database import Session
from .model import DNSHost

session = Session()


def handler(pkt):
    dns = pkt.getlayer("DNS")
    if dns is None:
        return

    try:
        ans_len = len(dns.an)
    except TypeError:
        return
    else:
        if ans_len > 0:
            idx = 0
            while True:
                try:
                    ans = dns.an[idx]
                except IndexError:
                    break

                host = ans.rrname.decode()

                try:
                    ip = ans.rdata.decode()
                except AttributeError:
                    ip = ans.rdata

                try:
                    session.add(DNSHost(host, ip))
                except ValueError:
                    continue

                idx += 1

            session.commit()
