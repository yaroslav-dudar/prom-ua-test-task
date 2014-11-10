from functools import wraps

from flask import (request, redirect, url_for, Flask, session,
    render_template)

from database import init_db
from decorators import login_required, login
from models import Book, Writer, User
from forms import (AuthForm, RegistrationForm, WriterEditForm,
    WriterAddForm, BookAddForm, BookEditForm)

app = Flask(__name__)
app.secret_key = 'A0Zr98j/MyXoR~hHH!jmN]LWX/,?RT'


@app.route('/', methods=['GET', 'POST'])
@login_required('all-users')
def index():
    if request.method == 'GET':
        return render_template('index.html', search_results='')
    else:
        search_query = request.form['search_query']
        search_results = Book.search_books(search_query)
        return render_template('index.html', search_results=search_results)


@app.route('/signup', methods=['GET', 'POST'])
@login
def signup():
    if request.method == 'GET':
        signup_form = RegistrationForm()
        return render_template('signup.html', error=False, form=signup_form)
    else:
        signup_form = RegistrationForm(request.form)
        if signup_form.validate():
            user = User.add(email=signup_form.email.data,
                password=signup_form.password.data, first_name=signup_form.first_name.data,
                last_name=signup_form.last_name.data, staff=False)
            session['user'] = user.email
            return redirect(url_for('index'))
        else:
            return render_template('signup.html', error=True, form=signup_form)


@app.route('/signin', methods=['GET', 'POST'])
@login
def signin():
    if request.method == 'GET':
        form = AuthForm()
        return render_template('signin.html', error=False, form=form)
    else:
        auth_form = AuthForm(request.form)
        if auth_form.validate():
            session['user'] = auth_form.email.data
            return redirect(url_for('index'))
        else:
            return render_template('signin.html', error=True, form=auth_form)


@app.route('/logout', methods=['GET'])
@login_required('all-users')
def logout():
    session.pop('user', None)
    return redirect(url_for('signin'))


@app.route('/writers', methods=['GET', 'POST'])
@login_required('staff-only')
def writers():
    writers = Writer.query.all()
    if request.method == 'GET':
        writer_add_form = WriterAddForm()
        writer_edit_form = WriterEditForm()
    else:
        if request.form['btn'] == 'Edit':
            # handle writers edit form
            writer_add_form = WriterAddForm()
            writer_edit_form = WriterEditForm(request.form)
            if writer_edit_form.validate():
                writer = Writer.query.filter_by(
                    id=writer_edit_form.id.data).first()
                writer.edit(name=writer_edit_form.name.data)
                return redirect(url_for('writers'))
        else:
            # handle writers add form
            writer_edit_form = WriterEditForm()
            writer_add_form = WriterAddForm(request.form)
            if writer_add_form.validate():
                Writer.add(name=writer_add_form.name.data)
                return redirect(url_for('writers'))
    return render_template('writers.html', writers=writers,
        writer_edit_form=writer_edit_form, writer_add_form=writer_add_form)


@app.route('/delete_writer/<int:writer_id>', methods=['GET', 'POST'])
@login_required('staff-only')
def delete_writer(writer_id):
    Writer.delete(writer_id)
    return redirect(url_for('writers'))


@app.route('/books', methods=['GET', 'POST'])
@login_required('staff-only')
def books():
    book_edit_form_errors = None
    book_edit_forms = []
    # generate book edit forms
    for book in Book.query.all():
        book_edit_form = BookEditForm()
        writers = Writer.query.all()
        book_edit_form.writers.data = [writer.id for writer in book.writers]
        book_edit_form.title.data = book.title
        book_edit_form.id.data = book.id
        book_edit_forms.append(book_edit_form)

    if request.method == 'GET':
        book_add_form = BookAddForm()
    else:
        if request.form['btn'] == 'Edit':
            book_add_form = BookAddForm()
            book_edit_form_errors = BookEditForm(request.form)
            if book_edit_form_errors.validate():
                writers = Writer.query.filter(Writer.id.in_(book_edit_form_errors.writers.data)).all()
                book = Book.query.filter(Book.id == book_edit_form_errors.id.data).first()
                book.edit(title=book_edit_form_errors.title.data, writers=writers)
                return redirect(url_for('books'))
        else:
            book_add_form = BookAddForm(request.form)
            if book_add_form.validate():
                writer_ids = [writer.id for writer in book_add_form.writers.data]
                writers = Writer.query.filter(Writer.id.in_(writer_ids)).all()
                Book.add(title=book_add_form.title.data, writers=writers)
                return redirect(url_for('books'))
    return render_template('books.html', book_add_form=book_add_form,
        book_edit_forms=book_edit_forms, book_edit_form_errors=book_edit_form_errors)


@app.route('/delete_book/<int:book_id>', methods=['GET', 'POST'])
@login_required('staff-only')
def delete_book(book_id):
    Book.delete(book_id)
    return redirect(url_for('books'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
