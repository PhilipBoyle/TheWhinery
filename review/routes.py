"""TODO: file to handle all of our app routes (@app_route("/")) e.t.c"""
from review import app
from flask import Flask, render_template
from flask import render_template, url_for, flash, redirect
from review.forms import RegistrationForm, LoginForm
from review.models import Account, Review
from review import db
from sqlalchemy import text



"""def sql_test():

    #db.execute("SELECT MAX price FROM review")
    sql = text("SELECT * FROM review WHERE country = 'Chile'")
    result = db.engine.execute(sql)
    names = []
    for row in result:
        names.append(row[0])
    print(names)
    return str(names)"""

@app.route('/')
@app.route('/home')
def home_page() -> 'html':
    return render_template('/review/base.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Account(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home_page'))
    return render_template('registration/register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('registration/login.html', title='Login', form=form)


@app.route('/review/<int:idnum>')
def review_detail(idnum):
    """ view single review in detail"""
    review = Review.query.get_or_404(idnum)
    return render_template('review/review_detail.html', title='Review Detail', review=review)


