# connect.py
import config
import psycopg2


# Conetando ao banco de dados PostgreSQL
def query(sql_query='', type='', list=None, debug=False, type_result='message',
            dcopy={}):
    conn = None
    message = ''
    try:
        # definindo parâmetros de conexão
        params = {'host': config.DATABASE_HOST,
                  'database': config.DATABASE,
                  'user': config.DATABASE_USER,
                  'password': config.DATABASE_PASSWORD,
                  'port': config.DATABASE_PORT}
        # print(debug, params)

        # conectando no banco PostgreSQL
        if debug:
            print('Conectando no banco de dados PostgreSQL "' + params['database'] + '" com o usuário "' + params['user'] + '" ...')

        conn = psycopg2.connect(**params)

        # criando cursor
        cursor = conn.cursor()
        if debug:
            print(type + ": ", sql_query)

        if type == 'sql':
            if list is not None:
                cursor.execute(sql_query, list)
            else:
                cursor.execute(sql_query)
            ## id = cursor.fetchone()[0]
            ## id = cursor.lastrowid
            if debug:
                # print("rowcount: ", cursor.rowcount)
                ## message = "return: {}".format(id)
                rowcount = cursor.rowcount
                lastrowid = cursor.lastrowid
                message = "return: {}{}".format(rowcount, lastrowid)
                print(message)
            conn.commit()

        elif type == 'multi-sql':
            if list is not None:
                cursor.executemany(sql_query, list)
            else:
                cursor.executemany(sql_query)
            ## row = cursor.fetchone()
            ## while row is not None:
            ##     ids.append(row)
            ##     row = cursor.fetchone()
            if debug:
                # print("rowcount: ", cursor.rowcount)
                ## ids = []
                ## message = "return: {}".format(ids)
                rowcount = cursor.rowcount
                lastrowid = cursor.lastrowid
                message = "return: {}{}".format(rowcount, lastrowid)
                print(message)
            conn.commit()

        elif type == 'copy-from':
            with open(dcopy['file'], 'r', encoding='utf-8') as f:
                next(f)  # Skip the header row.
                cursor.copy_from(file=f, table=dcopy['table'], sep=dcopy['sep'], null=dcopy['null'], columns=dcopy['columns'])
            f.close()

        elif type == 'copy-to':
            with open(dcopy['file'], 'r', encoding='utf-8') as f:
                next(f)  # Skip the header row.
                cursor.copy_to(file=f, table=dcopy['table'], sep=dcopy['sep'], null=dcopy['null'], columns=dcopy['columns'])
            f.close()

        elif type == 'copy-expert':
            with open(dcopy['file'], 'r', encoding='utf-8') as f:
                cursor.copy_expert(sql=sql_query, file=f)
            f.close()

        else:
            cursor.execute(sql_query)
            # blob = cursor.fetchone()
            results = cursor.fetchall()
            if debug:
                print("rowcount: ", cursor.rowcount)
                desc = [desc[0] for desc in cursor.description]
                print(desc)
                # print(str(blob[0]) + '|' + str(blob[1]) + '|' + str(blob[2]))
                # print(blob)
                for rec in results:
                    print(rec)

        # fechando comunicação com PostgreSQL
        cursor.close()

    except (Exception, psycopg2.DatabaseError) as error:
        message = '\nERROR: %s' % error + ' - ' + message
        print(message)
        return False
    finally:
        if conn is not None:
            conn.close()
            if debug:
                print('Conexão com o banco fechada.')

    if type_result == 'records':
        return results
    else:
        return message
