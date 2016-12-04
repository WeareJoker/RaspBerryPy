from sqlalchemy import Column, Integer, String

from database import Base


class DNS(Base):
    __tablename__ = 'dns'
    id = Column(Integer, primary_key=True)
    host = Column(String(30), nullable=False)

    def __init__(self, host):
        self.host = host

    def __repr__(self):
        return "<DNS %s>" % self.host


class Test(Base):
    __tablename__ = 'test'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Test %s>" % self.name
