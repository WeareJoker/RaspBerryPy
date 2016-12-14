from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "result.db")
engine = create_engine('sqlite:///{}'.format(db_path), echo=False)

Base = declarative_base()


class DNS(Base):
    __tablename__ = 'dns'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    ttl = Column(Integer, nullable=False)
    type = Column(String(100), nullable=False)
    data = Column(String(100), nullable=False)

    def __init__(self, name, ttl, typ, data):
        self.name = name
        self.ttl = ttl
        self.type = typ
        self.data = data

    def __repr__(self):
        return "<DNS %s>" % self.name


class Kakao(Base):
    __tablename__ = 'kakao'
    id = Column(Integer, primary_key=True)
    url = Column(String(100), nullable=False)

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return "<Kakao %s>" % self.url


class MailList(Base):
    __tablename__ = 'maillist'
    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False)
    usermail = Column(String(20), nullable=False)
    title = Column(String(100), nullable=False)
    sender_mail = Column(String(50), nullable=False)
    sender_name = Column(String(20), nullable=False)
    
    receiver_mail = Column(String(50), nullable=False)
    receiver_name = Column(String(20), nullable=False)
    sent_time = Column(String(30), nullable=False)

    def __init__(self, username, usermail, title, sender_mail, sender_name, receiver_mail,receiver_name, sent_time):
        self.username = username
        self.usermail = usermail
        self.title = title
        self.sender_mail = sender_mail
        self.sender_name = sender_name
        self.receiver_mail = receiver_mail
        self.receiver_name = receiver_name
        self.sent_time = sent_time

    def __repr__(self):
        return "<MailList %s>" % self.username

class CookieList(Base):
    __tablename__ = 'cookies'

    id = Column(Integer, primary_key=True)
    domain = Column(String(50), nullable=False)
    cookie = Column(String(3000), nullable=False)
    captured_time = Column(String(25), nullable=False)

    def __init__(self, domain, cookie, captured_time):
        self.domain = domain
        self.cookie = cookie
        self.captured_time = captured_time

    def __repr__(self):
        return "<Cookie %s>" % self.domain


class MailSize(Base):
    __tablename__ = 'mailsize'
    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False)
    title = Column(String(100), nullable=False)
    size = Column(String(50), nullable=False)
    folderName = Column(String(50), nullable=False)
    unreadCount = Column(String(100), nullable=False)
    totalCount = Column(String(50), nullable=False)

    def __init__(self, username, title, size, folderName, unreadCount, totalCount):
        self.username = username
        self.title = title
        self.size = size
        self.folderName = folderName
        self.unreadCount = unreadCount
        self.totalCount = totalCount

    def __repr__(self):
        return "<MailSize %s>" % self.username


Session = sessionmaker()
Session.configure(bind=engine)

Base.metadata.create_all(engine)

if __name__ == '__main__':
    session = Session()
    session.add(Kakao("testurl"))
    session.commit()
