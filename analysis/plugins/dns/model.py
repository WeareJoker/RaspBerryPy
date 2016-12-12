import re

from sqlalchemy import Column, Integer, String

from analysis.database import Base

host_rule = re.compile(
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?:/?|[/?]\S+)$', re.IGNORECASE
)


class DNSHost(Base):
    __tablename__ = 'dns'
    id = Column(Integer, primary_key=True)
    host = Column(String(30), nullable=False)
    ip = Column(String(30), nullable=False)

    def __init__(self, host, ip=None):
        self.host = host
        self.ip = ip
        self.validate_host()

    def __repr__(self):
        return "<DNS %s>" % self.host

    def validate_host(self):
        if host_rule.match(self.host) is None:
            raise ValueError
