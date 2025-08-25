"""
This is a utility module for providing DAO operations on a 
model class called Book
"""

from sqlalchemy import create_engine, Column, Integer, String, Double
from sqlalchemy.orm import declarative_base, sessionmaker
import json
from pprint import pprint

_db_engine = create_engine("sqlite:///booksdb.sqlite")
Session = sessionmaker(bind=_db_engine)

Base = declarative_base()


class Book(Base):
    """
    Model class for the application
    """
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    author = Column(String)
    publisher = Column(String)
    price = Column(Double)

    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        self.author = kwargs.get('author')
        self.price = kwargs.get('price')
        self.publisher = kwargs.get('publisher')

    def __repr__(self):
        return f'Book (title={self.title!r}, author={self.author!r}, price={self.price!r}, publisher={self.publisher!r})'


Base.metadata.create_all(_db_engine)


def add_book(book):
    """
    this methods adds a new book in the table
    """
    # do some basic validations on the book object
    with Session() as session:
        session.add(book)
        session.commit()
        print(book)
        return book
  

def get_all():
    """
    this method returns all books
    """
    with Session() as session: 
        return session.query(Book).all()


def get_by_id(book_id):
    with Session() as session:
        return session.get(Book, book_id)
    

class BookJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Book):
            d = o.__dict__
            if '_sa_instance_state' in d:
                d.pop('_sa_instance_state')
            return d
        return super().default(o)


if __name__ == '__main__':

    # all_books = get_all()
    # print(json.dumps(all_books, cls=BookJsonEncoder))

    book_id = 3
    b1 = get_by_id(book_id)
    if b1:
        print('Book found - ', b1)
        print(json.dumps(b1, cls=BookJsonEncoder))
    else:
        print(f'No book found with id {book_id}')

