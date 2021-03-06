from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

author_book_table = Table('author_book', Base.metadata,
                          Column('author_id', Integer, ForeignKey('author.id')),
                          Column('book_id', Integer, ForeignKey('book.id')))


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    isbn = Column(String(13), unique=True, nullable=True)
    title = Column(String, nullable=True)
    annotation = Column(String)
    authors = relationship('Author',
                           secondary=author_book_table,
                           backref='books')

    def __str__(self):
        return self.title
