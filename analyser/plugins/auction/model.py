from sqlalchemy import Column, Integer, String

from analyser.database import Base


class Auction(Base):
    __tablename__ = 'auction'
    id = Column(Integer, primary_key=True)
    username = Column(String(10), nullable=False)
    userid = Column(String(20), nullable=False)
    tel_home = Column(String(15), nullable=False)
    tel_mobile = Column(String(15), nullable=False)
    email = Column(String(30), nullable=False)
    address = Column(String(100))

    def __init__(self, username, userid, tel_home, tel_mobile, email, address=None):
        self.username = username
        self.userid = userid
        self.tel_home = tel_home
        self.tel_mobile = tel_mobile
        self.email = email
        self.address = address

    def __repr__(self):
        return "<Auction %s>" % self.username
