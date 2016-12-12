from sqlalchemy import Column, Integer, String

from analysis.database import Base


class Kakao(Base):
    __tablename__ = 'kakao'
    id = Column(Integer, primary_key=True)
    url = Column(String(100), nullable=False)

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return "<Kakao %s>" % self.url
