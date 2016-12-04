from .model import DNS
from database import Session

session = Session()


def handler(packet):
    session.add(DNS('www.naver.com'))
    session.commit()
    print packet
