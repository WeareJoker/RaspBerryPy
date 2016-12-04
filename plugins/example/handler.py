from .model import Example
from database import Session

session = Session()


def handler(packet):
    session.add(Example('www.naver.com'))
    session.commit()
    print packet
