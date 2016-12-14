import re
import functools

from scapy.all import *
from struct import unpack


class NoInfoException(Exception):
    pass


class InvalidInfoException(Exception):
    pass


class HTTPRequest:
    def __init__(self, payload):
        self.payload = payload
        self.request_object = self.get_http_request_object_list()
        self._cookie = None
        self._url = None
        self.host = self.get_host()

    def __repr__(self):
        return "<HTTPRequest %s>" % self.host

    def get_http_request_object_list(self):
        return self.payload.split('\r\n')

    def get_host(self):
        for request_object in self.request_object:
            if request_object.startswith("Host: "):
                return request_object.split(' ')[1]
        else:
            raise NoInfoException("No Host!!!")

    def get_cookie(self):
        cookie_head = "Cookie: "

        for obj in self.request_object:
            if obj.startswith(cookie_head):
                try:
                    return dict([(name, data)
                                 for name, data in [cookie.strip().split('=', 1)
                                                    for cookie in obj[len(cookie_head):].split('; ')]])
                except ValueError:
                    raise InvalidInfoException("Invalid Cookie!!!")
        else:
            return False

    def get_url(self):
        return self.host + self.request_object[0].split(' ')[1]

    @property
    def cookie(self):
        if self._cookie is None:
            self._cookie = self.get_cookie()

        return self._cookie

    @property
    def url(self):
        if self._url is None:
            self._url = self.get_url()

        return self._url


def parse_packet(packet):
    # parse ethernet header
    eth_length = 14

    eth_header = packet[:eth_length]
    eth = unpack('!6s6sH', eth_header)
    eth_protocol = socket.ntohs(eth[2])

    # Parse IP packets, IP Protocol number = 8
    if eth_protocol == 8:
        # Parse IP header
        # take first 20 characters for the ip header
        ip_header = packet[eth_length:20 + eth_length]

        # now unpack them :)
        iph = unpack('!BBHHHBBH4s4s', ip_header)

        version_ihl = iph[0]
        version = version_ihl >> 4
        ihl = version_ihl & 0xF

        iph_length = ihl * 4

        ttl = iph[5]
        protocol = iph[6]
        s_addr = socket.inet_ntoa(iph[8])
        d_addr = socket.inet_ntoa(iph[9])

        # TCP protocol
        if protocol == 6:
            t = iph_length + eth_length
            tcp_header = packet[t:t + 20]

            # now unpack them :)
            tcph = unpack('!HHLLBBHHH', tcp_header)

            source_port = tcph[0]

            dest_port = tcph[1]
            # print('Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(
            #    ttl) + ' Protocol : ' + str(
            #    protocol) + ' Source Address : ' + str(s_addr) + ' Destination Address : ' + str(d_addr))

            doff_reserved = tcph[4]
            tcph_length = doff_reserved >> 4

            # print('Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Sequence Number : ' +
            # str( sequence) + ' Acknowledgement : ' + str(acknowledgement) + ' TCP header length : ' + str(
            # tcph_length))

            h_size = eth_length + iph_length + tcph_length * 4

            # get data from the packet
            data = packet[h_size:]

            return data.decode()


def http_request_filter(filter_rule):
    def actual_http_filter(func):

        @functools.wraps(func)
        def wrapper(*args, **_):
            try:
                pkt = Ether(args[0])
                if pkt.getlayer("TCP").dport != 80:
                    raise AttributeError

                h = HTTPRequest(parse_packet(args[0]))

            except (NoInfoException, AttributeError):
                return
            else:
                if re.match(filter_rule, h.host) is None:
                    return
                else:
                    return func(h)

        return wrapper

    return actual_http_filter


def scapy_obj(func):
    def wrapper(*args, **kwargs):
        return func(Ether(args[0]))
    return wrapper
