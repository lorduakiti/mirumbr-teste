# importation.py
import config
from os.path import join, dirname
from zipfile import ZipFile


def dataset_extract():
    path = join(dirname(__file__), config.FILENAME_ZIP)
    filename = config.FILENAME_ZIP

    with ZipFile(filename, 'r') as zipObj:
        zipObj.extractall('datasets')


def main():
    dataset_extract()


if __name__ == '__main__':
    main()