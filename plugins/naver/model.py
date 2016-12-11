from sqlalchemy import Column, Integer, String

from database import Base


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

    def __init__(self, username, usermail, title, sender_mail, sender_name, receiver_mail, receiver_name, sent_time):
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
