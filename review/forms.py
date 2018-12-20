"""TODO: a file to handle the forms in the app eg: login, signup, data querying e.t.c"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField,RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class QueryForm(FlaskForm):
    qr1 = RadioField("", default='points', choices=[('points', 'points'), ('price', 'price')])
    qr2 = RadioField("", default='min', choices=[('min', 'min'), ('max', 'max'), ('avg', 'avg')])
    country = StringField('Country', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SearchBar(FlaskForm):
    choices = [('Description', 'Description'),
               ('Taster', 'Taster Name'),
               ('Country', 'Country')]
    search_type = SelectField('Search for wine:', choices=choices)
    search_term = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Login')
