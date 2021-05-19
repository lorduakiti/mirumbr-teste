# importation.py
import config
import os
import sys
from zipfile import ZipFile
import connect
import database
from fixit_dataset import fixit_file_dataset

path = os.path.dirname(__file__)
dataset = config.ZIP_FILENAME
path_file = os.path.join(path, dataset)
path_ds_folder = config.DS_FOLDER
ds_files = ['authors.csv', 'categories.csv', 'formats.csv', 'dataset.csv']
ds_columns = {
    'authors': ('author_id', 'author_name'),
    'categories': ('category_id', 'category_name'),
    'formats': ('format_id', 'format_name'),
    'dataset': ('author', 'bestsellers_rank', 'categorie', 'description', 'dimension_x', 'dimension_y', 'dimension_z',
                'edition', 'edition_statement', 'for_ages', 'format', 'id', 'illustrations_note',
                'image_checksum', 'image_path', 'image_url', 'imprint', 'index_date', 'isbn10', 'isbn13', 'lang',
                'publication_date', 'publication_place', 'rating_avg', 'rating_count', 'title', 'url', 'weight')
}


def delete_data():
    print("\nDeletando dados das tabelas...")
    import models
    models.Authors.query.delete()
    models.Categories.query.delete()
    models.Formats.query.delete()
    models.Dataset.query.delete()


def validate_tables_import():
    return True


def db_try_connection():
    sql_query = "select version();"
    result = connect.query(sql_query=sql_query, type='', list=None, debug=False, type_result='records')
    print(result)


def import_all():
    print("\nIniciando importação...")
    db_try_connection()

    try:
        # Limpando dados das tabelas
        delete_data()

        # Importação de dados em bloco por arquivo
        path_aux = os.path.join(path, path_ds_folder)
        for filename in ds_files:
            path_ds_file = os.path.join(path_aux, filename)
            table = filename.replace('.csv', '')

            print("Iniciando importação da tabela: ", table)
            if filename == 'dataset.csv':
                path_ds_file_new = path_ds_file.replace('.csv', '.sql')
                sql_file = open(path_ds_file_new, 'r', encoding='utf-8')
                # result = connect.query(sql_query=(sql_file.read()), type='sql', debug=False, type_result='message')
                # print('\n', path_ds_file_new, '\n', result)
                conn = database.engine.raw_connection()
                cursor = conn.cursor()
                # cursor.copy_expert(sql_file.read(), w)
                cursor.copy_expert(sql_file.readline(), w)
                conn.commit()

            else:
                with open(path_ds_file, 'rt', encoding='utf-8') as w:
                    copy_from = """
                        COPY """ + table + """ 
                        FROM STDIN
                        WITH (
                            FORMAT CSV,
                            DELIMITER '|',
                            ENCODING 'UTF8',
                            QUOTE '\"',
                            NULL 'NULL',
                            ESCAPE '\\',
                            HEADER
                        );
                        """
                    conn = database.engine.raw_connection()
                    cursor = conn.cursor()
                    cursor.copy_expert(copy_from, w)
                    conn.commit()
                w.close()

        print("Importação de tabelas concluída.")

    except Exception as err:
        print("Erro ao importar os dados das tabelas.")
        print(err)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def import_files(re_import):
    if not validate_tables_import():
        import_all()
    else:
        if re_import == '':
            print('\nOs dados já foram importados, \ngostaria de realizar a importação novamente (Y/n)?')
            re_import = input()
        if re_import.upper() == 'Y':
            import_all()


def fixit_files():
    # Ajustando cabeçalho do arquivo "dataset.csv"
    try:
        print('Iniciando ajuste de formatação dos arquivos extraídos...')
        path_aux = os.path.join(path, path_ds_folder)
        for filename in ds_files:
            path_ds_file = os.path.join(path_aux, filename)
            table = filename.replace('.csv', '')

            if filename == 'dataset.csv':
                fixit_file_dataset(path_aux, filename, (table + '.sql'))
            else:
                index_line = 0
                with open(path_ds_file, 'rt', encoding='utf-8-sig') as f:
                    text = f.readlines()
                    firstline = text[0]
                    new_firstline = firstline.replace('-', '_').replace('","', '"|"')
                    # if filename == 'dataset.csv':
                    #     new_firstline = new_firstline.replace('authors', 'author').replace('categories', 'categorie')

                with open(path_ds_file, 'w', encoding='utf-8-sig') as f:
                    for i in text:
                        if text.index(i) == index_line:
                            f.write(new_firstline)
                        else:
                            f.write(
                                i.replace('","', '"|"').replace('|""', '|NULL').replace('"[', '"{').replace(']"', '}"'))

            print("Ajustado cabeçalho e colunas do arquivo: ", filename)

    except Exception as err:
        print("Erro ao corrigir cabeçalho e nome de colunas dos arquivos.")
        print(err)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def validate_files_extracted():
    flag = True
    for f in ds_files:
        path_ds_file = os.path.join(path, path_ds_folder, f)
        if not os.path.exists(path_ds_file):
            flag = False
            break

    return flag


def extract_all():
    try:
        print('Iniciando extração de arquivos...')
        if os.path.exists(path_file):
            with ZipFile(dataset, 'r') as zipObj:
                zipObj.extractall(path_ds_folder)
            print('Arquivos extraídos.')

            fixit_files()

        else:
            print('Não foi possível encontrar o arquivo original de dados!', dataset)

    except Exception as err:
        print("Erro ao descompactar arquivo original de dados.")
        print(err)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def extrac_files(re_extrac=''):
    if not validate_files_extracted():
        extract_all()
    else:
        if re_extrac == '':
            print('\nOs arquivos de dados já foram descompatados, \ngostaria de realizar o processo novamente (Y/n)?')
            re_extrac = input()
        if re_extrac.upper() == 'Y':
            extract_all()


def main(re_extrac='', re_import=''):
    extrac_files(re_extrac)
    import_files(re_import)


if __name__ == '__main__':
    main()
