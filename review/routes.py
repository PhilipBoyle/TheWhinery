"""TODO: file to handle all of our app routes (@app_route("/")) e.t.c"""


from flask import Flask, render_template, request
from flask import url_for, flash, redirect
from flask_login import login_user, current_user, logout_user, login_required

from review import app
from review.forms import RegistrationForm, LoginForm, QueryForm, SearchBar, MakeReview
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
    """home page route"""
    return render_template('/review/home.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    """ allows user to register, posts the user info to the Account table in our database"""
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Account(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('registration/register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """ logs the user in, if the are already loged in it redirects to homepage"""
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
    """ logs the user out and redirects them back to the home page"""
    logout_user()
    return redirect(url_for('home_page'))


@app.route('/review/<int:idnum>')
@login_required
def review_detail(idnum):
    """ view single review in detail"""
    review = Review.query.get_or_404(idnum)
    return render_template('review/review_detail.html', title='Review Detail', review=review)


@app.route('/query', methods=['GET', 'POST'])
@login_required
def query():  # search):
    """ main query function, allows user to query the data base for min/max/avg by price/score in a country"""
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
@login_required
def search():
    """main search function, searches either descrpiton,taster or country by a user input string"""
    form = SearchBar(request.form)
    if form.validate_on_submit():
        print('valid')
        return redirect((url_for('search_results', search_word=form.search_term.data,
                                 search_type=form.search_type.data)))
    print('invalid')
    return render_template('review/search.html', form=form)


@app.route('/search_results/<string:search_type>/<string:search_word>',  methods=['GET', 'POST'])
@login_required
def search_results(search_word, search_type):
    """ results output for search"""
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


@app.route('/chart', methods=[ 'GET', 'POST'])
@login_required
def chart():
    wine_countries = {}
    for qry in db.session.query(Review.country): 
        if qry.country in wine_countries:
            wine_countries[qry.country] += 1
        else:
            wine_countries[qry.country] = 1
    print(str(wine_countries))
    num_countries = len(wine_countries)
    print( num_countries )
    return render_template('chart/chart.html', title='Chart Results', wd=wine_countries)


@app.route('/add_review', methods=['GET', 'POST'])
def make_review():
    """allows user to make a review and add it to the database"""
    form = MakeReview()
    if form.validate_on_submit():
        review = Review(
            points=form.points.data,
            title=form.title.data,
            description=form.description.data,
            taster_name=form.taster_name.data,
            taster_twitter_handle=form.taster_twitter_handle.data,
            price=form.price.data,
            designation=form.designation.data,
            variety=form.variety.data,
            region_1=form.region_1.data,
            region_2=form.region_2.data,
            province=form.province.data,
            country=form.country.data,
            winery=form.winery.data
        )
        db.session.add(review)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home_page'))
    return render_template('review/add_review.html', title='New Post',
                           form=form)


@app.route("/post/<int:idnum>/delete", methods=['POST', 'GET'])
@login_required
def delete_review(idnum):
    """allows user to delete a review, button available on the review detail page"""
    review = Review.query.get_or_404(idnum)
    db.session.delete(review)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home_page'))

