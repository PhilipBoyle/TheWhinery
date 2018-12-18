from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:password@localhost:5432/test_wine'
try:
	db = SQLAlchemy(app)
	print ("it worked ????")
except:
	print ("didn't work")

from review import routes