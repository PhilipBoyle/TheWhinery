from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://student7:student:123@206.189.124.205:5432/northwind7'
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
try:
	db = SQLAlchemy(app)
	print("it worked ????")
except:
	print("didn't work")

from review import routes
