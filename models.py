# models.py
from sqlalchemy import (Column, Index, Date, DateTime, Numeric, Integer, BigInteger, String, Text, ForeignKey, Boolean, JSON, ARRAY)
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

    def to_json(self):
        return {"author_id": self.author_id, "author_name": self.author_name}


class Categories(Base):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(500))

    def __init__(self, category_name=None):
        self.category_name = category_name

    def __repr__(self):
        return f'<Categories {self.category_name!r}>'

    def to_json(self):
        return {"category_id": self.category_id, "category_name": self.category_name}


class Formats(Base):
    __tablename__ = 'formats'
    format_id = Column(Integer, primary_key=True)
    format_name = Column(String(50), unique=True)

    def __init__(self, format_name=None):
        self.format_name = format_name

    def __repr__(self):
        return f'<Formats {self.format_name!r}>'

    def to_json(self):
        return {"format_id": self.format_id, "format_name": self.format_name}


class Dataset(Base):
    __tablename__ = 'dataset'
    author = Column(ARRAY(Integer))  # ForeignKey('authors.author_id'))
    bestsellers_rank = Column(Numeric(20, 2))
    categorie = Column(ARRAY(Integer))  # ForeignKey('categories.category_id'))
    description = Column(Text)
    dimension_x = Column(Numeric(20, 2))
    dimension_y = Column(Numeric(20, 2))
    dimension_z = Column(Numeric(20, 2))
    edition = Column(String(100))
    edition_statement = Column(String(100))
    for_ages = Column(String(10))
    format = Column(Integer, ForeignKey('formats.format_id'))
    id = Column(BigInteger, primary_key=True)
    illustrations_note = Column(String(500))
    image_checksum = Column(String(500))
    image_path = Column(String(500))
    image_url = Column(String(500))
    imprint = Column(String(300))
    index_date = Column(String(100))
    isbn10 = Column(String(100))
    isbn13 = Column(BigInteger)
    lang = Column(String(10))
    publication_date = Column(DateTime)
    publication_place = Column(String(100))
    rating_avg = Column(Numeric(20, 2))
    rating_count = Column(Numeric(20, 2))
    title = Column(String(500))
    url = Column(String(500))
    weight = Column(Numeric(20, 2))
    # authors = relationship("Authors")
    # categories = relationship("Categories")
    formats = relationship("Formats")

    def __init__(self, **kwargs):
        self.author = kwargs.get('author')
        self.categorie = kwargs.get('categorie')
        self.format = kwargs.get('format')

    def __repr__(self):
        return f'{self.title}, {self.author}, {self.categorie}, {self.format}'

    def to_json(self):
        return {
            "author": self.author,
            "bestsellers_rank": self.bestsellers_rank,
            "categorie": self.categorie,
            "description": self.description,
            "dimension_x": self.dimension_x,
            "dimension_y": self.dimension_y,
            "dimension_z": self.dimension_z,
            "edition": self.edition,
            "edition_statement": self.edition_statement,
            "for_ages": self.for_ages,
            "format": self.format,
            "id": self.id,
            "illustrations_note": self.illustrations_note,
            "image_checksum": self.image_checksum,
            "image_path": self.image_path,
            "image_url": self.image_url,
            "imprint": self.imprint,
            "index_date": self.index_date,
            "isbn10": self.isbn10,
            "isbn13": self.isbn13,
            "lang": self.lang,
            "publication_date": self.publication_date,
            "publication_place": self.publication_place,
            "rating_avg": self.rating_avg,
            "rating_count": self.rating_count,
            "title": self.title,
            "url": self.url,
            "weight": self.weight
        }

