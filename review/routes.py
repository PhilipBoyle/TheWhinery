"""TODO: file to handle all of our app routes (@app_route("/")) e.t.c"""


from flask import Flask, render_template, request
from flask import url_for, flash, redirect
from flask_login import login_user, current_user, logout_user, login_required

from review import app
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
    return render_template('/review/home.html')


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
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Account.query.filter_by(email=form.email.data).first()
        if user and (user.password == form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home_page'))

        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('registration/login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home_page'))


@app.route('/review/<int:idnum>')
def review_detail(idnum):
    """ view single review in detail"""
    review = Review.query.get_or_404(idnum)
    return render_template('review/review_detail.html', title='Review Detail', review=review)


@app.route('/search')
def search():  # search_word):
    review = Review.query.get_or_404
    results = Review.query.filter(Review.description.contains('sweet')).all()
    # results = Review.query.filter(Review.description.contains(search_word)).all()
    return render_template('review/search_results.html', title="Search Results", review=review, results=results)  # ,search_word=search_word)

