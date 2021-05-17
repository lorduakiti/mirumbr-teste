# config.py
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DATABASE = os.environ.get("DATABASE")
DATABASE_HOST = os.environ.get("DATABASE_HOST")
DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_PORT = os.environ.get("DATABASE_PORT")

SECRET_KEY = os.environ.get("SECRET_KEY")

ZIP_FILENAME = os.environ.get("ZIP_FILENAME")
DS_FOLDER = os.environ.get("DS_FOLDER")
