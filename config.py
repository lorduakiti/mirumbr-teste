# config.py
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DATABASE = os.environ.get("DATABASE")
DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_PORT = os.environ.get("DATABASE_PORT")

SECRET_KEY = os.environ.get("SECRET_KEY")
FILENAME_ZIP = os.environ.get("FILENAME_ZIP")
