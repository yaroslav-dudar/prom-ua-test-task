from functools import wraps

from flask import request, redirect, url_for, Flask, session
from flask import render_template

from database import init_db
from database import db_session

from models import Book, Writer, User
from forms import (AuthForm, RegistrationForm, WriterEditForm,
    WriterAddForm, BookAddForm)

app = Flask(__name__)
app.secret_key = 'A0Zr98j/MyXoR~hHH!jmN]LWX/,?RT'

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session.get('user', None):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('signin', next=request.url))
    return decorated_function


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    writers = Writer.query.all()
    writer_form = WriterEditForm()
    writer_add_form = WriterAddForm()
    book_add_form = BookAddForm()
    return render_template('index.html', search_results='',
        writers=writers, writer_edit_form=writer_form,
        writer_add_form=writer_add_form, book_add_form=book_add_form)
    

@app.route('/search',  methods=['POST'])
@login_required
def search():
    if request.method == 'POST':
        search_query = request.form['search_query']
        search_results = Book.search_books(search_query)
    else:
        search_results = None
    return render_template('index.html', search_results=search_results)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        signup_form = RegistrationForm()
        return render_template('signup.html', error=False, form=signup_form)
    else:
        signup_form = RegistrationForm(request.form)
        if signup_form.validate():
            # drag to User class!!!
            user = User(email=signup_form.email.data,
                password=signup_form.password.data, first_name=signup_form.first_name.data,
                last_name=signup_form.last_name.data, staff=False)
            db_session.add(user)
            db_session.commit()
            session['user'] = user.email
            return redirect(url_for('index'))
        else:
            return render_template('signup.html', error=True, form=signup_form)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        form = AuthForm()
        return render_template('signin.html', error=False, form=form)
    else:
        auth_form = AuthForm(request.form)
        if auth_form.validate():
            print auth_form.email.data
            session['user'] = auth_form.email.data
            return redirect(url_for('index')) 
        else:
            return render_template('signin.html', error=True, form=auth_form)


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user', None)
    return redirect(url_for('signin'))


@app.route('/edit_writer', methods=['POST'])
@login_required
def edit_writer():
    form = WriterEditForm(request.form)
    if form.validate():
        writer = db_session.query(Writer).filter_by(id=form.id.data).first()
        writer.name = form.name.data
        db_session.commit()
        return redirect(url_for('index'))
    else:
        writers = Writer.query.all()
        writer_add_form = WriterAddForm()
        return render_template('index.html', search_results='',
            writers=writers, writer_edit_form=form,
            writer_add_form=writer_add_form)


@app.route('/add_writer', methods=['POST'])
@login_required
def add_writer():
    form = WriterAddForm(request.form)
    if form.validate():
        writer = Writer(name=form.name.data)
        db_session.add(writer)
        db_session.commit()
        return redirect(url_for('index'))
    else:
        writers = Writer.query.all()
        writer_edit_form = WriterEditForm()
        return render_template('index.html', search_results='',
            writers=writers, writer_edit_form=writer_edit_form,
            writer_add_form=form)


@app.route('/delete_writer/<int:writer_id>', methods=['GET', 'POST'])
@login_required
def delete_writer(writer_id):
    writer = db_session.query(Writer).filter(Writer.id == writer_id).first()
    db_session.delete(writer)
    db_session.commit()
    return redirect(url_for('index'))

@app.route('/add_book', methods=['POST'])
def add_book():
    form = BookAddForm(request.form)
    writer_ids = [writer.id for writer in form.writers.data]
    if form.validate():
        writers = db_session.query(Writer).filter(Writer.id.in_(writer_ids)).all()
        book = Book(title=form.title.data, writers=writers)
        db_session.add(book)
        db_session.commit()
        return redirect(url_for('index'))
    else:
        writers = Writer.query.all()
        writer_edit_form = WriterEditForm()
        writer_add_form = WriterAddForm()
        return render_template('index.html', search_results='',
            writers=writers, writer_edit_form=writer_edit_form,
            writer_add_form=writer_add_form, book_add_form=form)        

    


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
