from sqlalchemy import Column, Integer, String, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import or_

from database import Base
from database import db_session

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
		result = db_session.query(Book).join(
			Book.writers, Writer).filter(or_(
			Book.title == query, Writer.name == query)).all()
		return result


class Writer(Base):
	__tablename__ = 'writers'
	id = Column(Integer, primary_key=True)
	name = Column(String)

	def __repr__(self):
		return self.name


class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	email = Column(String, unique=True, nullable = False)
	password = Column(String, nullable = False)
	first_name = Column(String)
	last_name = Column(String)
	staff = Column(Boolean)
