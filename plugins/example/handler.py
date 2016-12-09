from database import Session

session = Session()


def handler(ether):
    packet = ether
#    ip = ether.child()
#    proto = ip.child()
#    if proto.get_th_dport() == 80:  # if http packet
#   data = proto.child()
#        print data.get_buffer_as_string()

