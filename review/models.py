"""TODO: Create User Model. Create Review Model using "AutoMap" 
(research that, its used when using existing databases)"""
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from review import db
from sqlalchemy.orm import relationship, backref

engine = create_engine('postgresql+psycopg2://postgres:password@localhost:5432/the_whinery')
# engine.set_client_encoding('utf-8')

#Base = declarative_base()


class Account(db.Model):
    """"""
    __tablename__ = "account"
 
    id = db.Column(Integer, primary_key=True)
    username = db.Column(String)
    email = db.Column(String)
    password = db.Column(String)


class Review(db.Model):

    __tablename__ = "review"

    IDnum = db.Column(Integer, primary_key=True)
    points = db.Column(Integer)
    title = db.Column(String)
    description = db.Column(String)
    taster_name = db.Column(String)
    taster_twitter_handle = db.Column(String)
    price = db.Column(Integer)
    designation = db.Column(String)
    variety = db.Column(String)
    region_1 = db.Column(String)
    region_2 = db.Column(String)
    province = db.Column(String)
    country = db.Column(String)
    winery = db.Column(String)
