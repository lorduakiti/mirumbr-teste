# database.py
import config
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


database_uri = 'postgresql://' + \
               config.DATABASE_USER + ':' + \
               config.DATABASE_PASSWORD + '@' + config.DATABASE_HOST + ':' + \
               config.DATABASE_PORT + '/' + \
               config.DATABASE
engine = create_engine(database_uri)
db_session = scoped_session(
    sessionmaker(autocommit=False,
                 autoflush=False,
                 bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import models
    Base.metadata.create_all(bind=engine)