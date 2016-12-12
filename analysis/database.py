# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# engine = create_engine('sqlite:///result.db', echo=True)
engine = create_engine('sqlite:///result.db')
Base = declarative_base(engine)
Session = sessionmaker(bind=engine)
