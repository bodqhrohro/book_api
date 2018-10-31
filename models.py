from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    photo = Column(String(255)) # filename

    def __str__(self):
        return self.name

class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    isbn = Column(String(13), unique=True, nullable=True)
    title = Column(String, nullable=True)
    annotation = Column(String)
    authors = Column(Integer, ForeignKey(Author.id))
    cover = Column(String(255)) # filename

    def __str__(self):
        return self.title
