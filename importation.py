# importation.py
import config
import os
from zipfile import ZipFile
import connect
import database

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


def fixit_files():
    # Ajustando cabeçalho do arquivo "dataset.csv"
    try:
        for filename in ds_files:
            path_ds_file = os.path.join(path, path_ds_folder, filename)
            index_line = 0
            with open(path_ds_file, 'rt', encoding='utf-8-sig') as f:
                text = f.readlines()
                firstline = text[0]
                new_firstline = firstline.replace('-', '_').replace('","', '"|"')
                if filename == 'dataset.csv':
                    new_firstline = new_firstline.replace('authors', 'author').replace('categories', 'categorie')

            with open(path_ds_file, 'w', encoding='utf-8-sig') as f:
                for i in text:
                    if text.index(i) == index_line:
                        f.write(new_firstline)
                    else:
                        f.write(i.replace('","', '"|"').replace('|""', '|NULL').replace('"[', '"{').replace(']"', '}"'))
                        # 3390 | 10181 | 18361 .. linhas com erro no char de quebra de linha
                        # n]"|"  .]"|  '->`  ""->"  ;->? '->?  ;}'->?  '{->? .. caractéres especiais nos textos
                        # NULL" -> NULL,"   ,NULL"->,NULL,'

            print("Ajustado cabeçalho e colunas do arquivo: ", filename)

    except Exception as e:
        print("Erro ao corrigir cabeçalho e nome de colunas dos arquivos.", e)


def dataset_extract():
    try:
        if os.path.exists(path_file):
            with ZipFile(dataset, 'r') as zipObj:
                zipObj.extractall(path_ds_folder)
            fixit_files()
            print('Arquivos extraídos.')
        else:
            print('Não foi possível encontrar o arquivo original de dados!', dataset)
    except Exception as e:
        print("Erro ao descompactar arquivo original de dados.", e)


def validate_files_extracted():
    flag = True
    for f in ds_files:
        path_ds_file = os.path.join(path, path_ds_folder, f)
        if not os.path.exists(path_ds_file):
            flag = False
            break

    return flag


def delete_data():
    import models
    models.Authors.query.delete()
    models.Categories.query.delete()
    models.Formats.query.delete()
    models.Dataset.query.delete()

def db_try_connection():
    sql_query = "select version();"
    result = connect.query(sql_query=sql_query, type='', list=None, debug=False, type_result='records')
    print(result)

def import_files():
    db_try_connection()

    try:
        # Limpando dados das tabelas
        # delete_data()

        # Importação de dados em bloco por arquivo
        for filename in ds_files:
            path_ds_file = os.path.join(path, path_ds_folder, filename)
            table = filename.replace('.csv', '')
            # public.categories (category_id, category_name)
            print("Iniciando importação da tabela: ", table)
            # connect.query(type='copy-file', debug=True,
            #               dcopy={
            #                   'file': path_ds_file,
            #                   'table': table,
            #                   'sep': ',',
            #                   'columns': ds_columns[table]
            #               })

            with open(path_ds_file, 'rt', encoding='utf-8') as w:
                # DELIMITER ',' CSV HEADER ENCODING 'UTF8' QUOTE '\"' NULL 'NULL' ESCAPE '''';""
                # copy_from = "COPY " + table + "  TO STDIN WITH CSV ENCODING 'UTF8' DELIMITER ',' QUOTE '\"' NULL 'NULL' HEADER  "
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
    except Exception as e:
        print("Erro ao importar os dados das tabelas.", e)


def extrac_files(re_extrac=''):
    if not validate_files_extracted():
        dataset_extract()
    else:
        if re_extrac == '':
            print('Os arquivos de dados já foram descompatados, gostaria de realizar o processo novamente (Y/n)?')
            re_extrac = input()
        if re_extrac.upper() == 'Y':
            dataset_extract()


def main(re_extrac=''):
    extrac_files(re_extrac)
    import_files()


if __name__ == '__main__':
    main()
