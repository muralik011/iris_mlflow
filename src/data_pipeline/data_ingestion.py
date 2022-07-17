from utils.secrets_parser import SecretsParser
import psycopg2
import pandas as pd




def connect_postgres():
    try:
        secrets_parser = SecretsParser()
        db_connection = psycopg2.connect(host=secrets_parser.get_values(['data_source', 'host']),
                                         database=secrets_parser.get_values(['data_source', 'database']),
                                         user=secrets_parser.get_values(['data_source', 'username']),
                                         password=secrets_parser.get_values(['data_source', 'password'])
                                         )
    except Exception as conn_exception:
        print(f'UNABLE TO CONNECT TO DB SERVER\nREASON: {conn_exception}')
        return None
    else:
        print('DB SERVER CONNECTION SUCCESSFUL')
        return db_connection

def read_table_from_database(db_connection):
    secrets_parser = SecretsParser()
    df = None
    if db_connection is not None:
        table = secrets_parser.get_values(['data_source', 'table'])
        cursor = db_connection.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        df = pd.DataFrame(cursor.fetchall())
        df.columns = [col_name[0] for col_name in cursor.description]
        cursor.close()
        db_connection.close()
    return df

print(read_table_from_database(connect_postgres()))

