"""TODO: Create User Model. Create Review Model using "AutoMap" 
(research that, its used when using existing databases)"""
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('postgresql+psycopg2://postgres:password@localhost:5432/test_wine')
engine.set_client_encoding('utf-8')

Base = declarative_base()


class user(Base):
    """"""
    __tablename__ = "users"
 
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
	
	__