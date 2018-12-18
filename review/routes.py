"""TODO: file to handle all of our app routes (@app_route("/")) e.t.c"""
from review import app
from flask import Flask, render_template

@app.route('/')
@app.route('/home')
def Home_page() -> 'html':
    return render_template('/review/base.html')