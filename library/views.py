from flask import request, redirect, url_for, Flask, session
from flask import render_template

from database import init_db
from database import db_session

from models import Book, Writer, User
from forms import AuthForm, RegistrationForm

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'GET':
		auth_form = AuthForm()
		return render_template('index.html', books='', form=auth_form)
	else:
		# login
		auth_form = AuthForm(request.form)
		if auth_form.validate():
			error = False
			session['user'] = True
		else:
			error = True
		return render_template('index.html',
			books='', form=auth_form, error=error)


@app.route('/search',  methods=['POST'])
def search():
	if request.method == 'POST':
		search_query = request.form['search_query']
		books = Book.search_books(search_query)
	else:
		books = None
	return render_template('index.html', books=books)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'GET':
		signup_form = RegistrationForm()
		return render_template('signup.html', error=False, form=signup_form)
	else:
		signup_form = RegistrationForm(request.form)
		if signup_form.validate():
			user = User(email=signup_form.email.data,
				password=signup_form.password.data, first_name=signup_form.first_name.data,
				last_name=signup_form.last_name.data, staff=False)
			db_session.add(user)
			db_session.commit()

			return redirect(url_for('index'))
		else:
			return render_template('signup.html', error=True, form=signup_form)

if __name__ == '__main__':
	init_db()
	app.run(debug=True)