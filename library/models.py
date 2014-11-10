from sqlalchemy import Column, Integer, String, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import or_

from database import Base, db_session

association_table = Table('association', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id')),
    Column('writer_id', Integer, ForeignKey('writers.id'))
)


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    writers = relationship('Writer', secondary=association_table)

    def __repr__(self):
        return self.title

    @staticmethod
    def search_books(query):
        """ Search Books by writer.name, book.title """
        result = Book.query.join(
            Book.writers, Writer).filter(or_(
            Book.title == query, Writer.name == query)).all()
        return result

    @staticmethod
    def delete(book_id):
        book = Book.query.filter_by(id=book_id).first()
        if book:
            db_session.delete(book)
            db_session.commit()

    @staticmethod
    def add(title, writers):
        book = Book(title=title, writers=writers)
        db_session.add(book)
        db_session.commit()

    def edit(self, title, writers):
        self.title = title
        self.writers = writers
        #db_session.add(self)
        db_session.commit()


class Writer(Base):
    __tablename__ = 'writers'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return self.name

    @staticmethod
    def delete(writer_id):
        writer = Writer.query.filter_by(id=writer_id).first()
        if writer:
            db_session.delete(writer)
            db_session.commit()

    @staticmethod
    def add(name):
        writer = Writer(name=name)
        if writer:
            db_session.add(writer)
            db_session.commit()

    def edit(self, name):
        self.name = name
        db_session.commit()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    staff = Column(Boolean, default=True)

    @staticmethod
    def add(email, password, first_name, last_name, staff):
        user = User(email=email, password=password, first_name=first_name,
            last_name=last_name, staff=staff)
        db_session.add(user)
        db_session.commit()
        return user
