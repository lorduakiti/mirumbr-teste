# models.py
from sqlalchemy import (Column, Index, Date, DateTime, Numeric, Integer, BigInteger, String, Text, ForeignKey, Boolean, JSON)
from sqlalchemy.orm import relationship

from database import Base

class Authors(Base):
    __tablename__ = 'authors'
    author_id = Column(Integer, primary_key=True)
    author_name = Column(String(250), unique=True)

    def __init__(self, author_name=None):
        self.author_name = author_name

    def __repr__(self):
        return f'<Authors {self.author_name!r}>'


class Categories(Base):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(500), unique=True)

    def __init__(self, category_name=None):
        self.category_name = category_name

    def __repr__(self):
        return f'<Categories {self.category_name!r}>'


class Formats(Base):
    __tablename__ = 'formats'
    format_id = Column(Integer, primary_key=True)
    format_name = Column(String(50), unique=True)

    def __init__(self, format_name=None):
        self.format_name = format_name

    def __repr__(self):
        return f'<Formats {self.format_name!r}>'


class Dataset(Base):
    __tablename__ = 'dataset'
    id = Column(Integer, primary_key=True)
    author = Column(Integer, ForeignKey('authors.author_id'))
    bestsellers_rank = Column(Numeric(20, 2))
    categorie = Column(JSON, ForeignKey('categories.category_id'))
    description = Column(Text)
    dimension_x = Column(Numeric(20, 2))
    dimension_y = Column(Numeric(20, 2))
    dimension_z = Column(Numeric(20, 2))
    edition = Column(String(100))
    edition_statement = Column(String(100))
    for_ages = Column(String(10))
    format = Column(Integer, ForeignKey('formats.format_id'))
    illustrations_note = Column(String(100))
    image_checksum = Column(String(500))
    image_path = Column(String(500))
    image_url = Column(String(500))
    imprint = Column(String(300))
    index_date = Column(String(100))
    isbn10 = Column(String(100))
    isbn13 = Column(Integer)
    lang = Column(String(10))
    publication_date = Column(DateTime, nullable=False)
    publication_place = Column(String(100))
    rating_avg = Column(Numeric(20, 2))
    rating_count = Column(Numeric(20, 2))
    title = Column(String(500))
    url = Column(String(500))
    weight = Column(Numeric(20, 2))
    authors = relationship("Authors")
    categories = relationship("Categories")
    formats = relationship("Formats")

    def __init__(self, **kwargs):
        self.author = kwargs.get('author')
        self.categorie = kwargs.get('categorie')
        self.format = kwargs.get('format')

    def __repr__(self):
        return f'{self.title}, {self.author}, {self.categorie}, {self.format}'

