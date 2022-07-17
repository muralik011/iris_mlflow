from utils.json_parser import JSONParser
import psycopg2
import pandas as pd
import os


def connect_postgres():
    try:
        secrets_parser = JSONParser("secrets.json")
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
    secrets_parser = JSONParser("secrets.json")
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


def save_raw_data():
    df = read_table_from_database(connect_postgres())
    config_parser = JSONParser('config.json')
    raw_data_dir = config_parser.get_values(['data_folder', 'raw'])
    df.to_csv(os.path.join('data', raw_data_dir, 'iris.csv'), index=False)

if __name__ == "__main__":
    save_raw_data()
