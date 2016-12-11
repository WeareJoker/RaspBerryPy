from sqlalchemy import Column, Integer, String

from database import Base


class DNSHost(Base):
    __tablename__ = 'dns'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    ip = Column(String(30))

    def __init__(self, name, ip=None):
        self.name = name
        self.ip = ip

    def __repr__(self):
        return "<DNS %s>" % self.name
