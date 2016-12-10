from database import Session

session = Session()


def handler(ether):
    ip = ether.child()
    proto = ip.child()
    try:
        port = proto.get_th_dport()
    except AttributeError:
        pass
    else:
        if port == 80:  # if http packet
            data = proto.child()
            print data.get_buffer_as_string()

