"""TODO: Create User Model. Create Review Model using "AutoMap" 
(research that, its used when using existing databases)"""
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from review import db, login_manager
from sqlalchemy.orm import relationship, backref
from flask_login import UserMixin

engine = create_engine('postgresql+psycopg2://student7:student:123@206.189.124.205:5432/northwind7')
# engine.set_client_encoding('utf-8')

#Base = declarative_base()

@login_manager.user_loader
def load_user(id):
    return Account.query.get(int(id))


class Account(db.Model, UserMixin):
    """"""
    __tablename__ = "account"
 
    id = db.Column(Integer, primary_key=True)
    username = db.Column(String, unique=True)
    email = db.Column(String, unique=True)
    password = db.Column(String)


class Review(db.Model):

    __tablename__ = "review"

    idnum = db.Column(Integer, primary_key=True)
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
