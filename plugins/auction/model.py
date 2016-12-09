from sqlalchemy import Column, Integer, String

from database import Base


class Auction(Base):
    __tablename__ = 'auction'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(10), nullable=False)
    user_id = Column(String(20), nullable=False)
    tel_home = Column(String(15), nullable=False)
    tel_mobile = Column(String(15), nullable=False)
    email = Column(String(30), nullable=False)
    address = Column(String(50))

    def __init__(self, user_name, user_id, tel_home, tel_mobile, email, address):
        self.user_name = user_name
        self.user_id = user_id
        self.tel_home = tel_home
        self.tel_mobile = tel_mobile
        self.email = email
        self.address = address

    def __repr__(self):
        return "<Example %s>" % self.user_name
