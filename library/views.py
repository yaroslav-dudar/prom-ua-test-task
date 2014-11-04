from flask import Flask
from flask import request
from flask import render_template

from database import init_db
from database import db_session

from models import Book, Writer

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('base.html', books='')


@app.route('/search',  methods=['POST'])
def search():
	if request.method == 'POST':
		search_query = request.form['search_query']
		books = Book.search_books(search_query)
	else:
		books = None
	return render_template('base.html', books=books)

if __name__ == '__main__':
	init_db()
	app.run(debug=True)