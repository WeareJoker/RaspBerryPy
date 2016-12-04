from sqlalchemy import Column, Integer, String

from database import Base


class Example(Base):
    __tablename__ = 'example'
    id = Column(Integer, primary_key=True)
    data = Column(String(30), nullable=False)

    def __init__(self, host):
        self.host = host

    def __repr__(self):
        return "<Example %s>" % self.data
