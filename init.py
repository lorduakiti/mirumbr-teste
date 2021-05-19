from database import init_db
from importation import exec_importation

if __name__ == '__main__':
    init_db()
    exec_importation(re_extrac='Y', re_import='Y')