"""TODO: file to handle all of our app routes (@app_route("/")) e.t.c"""


from flask import Flask, render_template, request
from flask import url_for, flash, redirect
from flask_login import login_user, current_user, logout_user, login_required

from review import app
from review.forms import RegistrationForm, LoginForm, QueryForm, SearchBar
from review.models import Account, Review
from review import db
from sqlalchemy import desc

from sqlalchemy import func, and_


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



@app.route('/query', methods=['GET', 'POST'])
def query():  # search):
    form = QueryForm()
    query_dict = {'points': Review.points, 'price': Review.price, 'max': db.func.max, 'min': db.func.min, 'avg': db.func.avg}

    if form.validate_on_submit():
        subq = db.session.query(query_dict[form.qr2.data](query_dict[form.qr1.data])).filter(Review.country == form.country.data)
        x=[]
        for r in subq:
            x=r
            print(r)
        print (x[0])
        q = Review.query.filter(Review.country == form.country.data, query_dict[form.qr1.data] == int(x[0])).all()

        return render_template('query/minmaxavg.html', title='Results', q=q)
    
    return render_template('query/query_form.html', title='Results', form=form)

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchBar(request.form)
    if form.validate_on_submit():
        print('valid')
        return redirect((url_for('search_results', search_word=form.search_term.data,
                                 search_type=form.search_type.data)))
    print('invalid')
    return render_template('review/search.html', form=form)


@app.route('/search_results/<string:search_type>/<string:search_word>',  methods=['GET', 'POST'])
def search_results(search_word, search_type):
    search_table = Review.country
    if search_type == 'Country':
        search_table = Review.country
    if search_type == 'Description':
        search_table = Review.description
    if search_type == 'Taster':
        search_table = Review.taster_name

    review = Review()
    results = Review.query.filter(search_table.contains(search_word)).order_by(desc(Review.points)).all()
    return render_template('review/search_results.html', search_word=search_word, search_type=search_type,
                           results=results, review=review)

