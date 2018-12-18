"""This will be the small python file to run the webapp when we are done"""

from review import app

if __name__ == '__main__':
    app.run(debug=True)