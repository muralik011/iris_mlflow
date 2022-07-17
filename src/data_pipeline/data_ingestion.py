from src.utils.json_parser import JSONParser
import psycopg2
import pandas as pd
import os


def connect_postgres():
    try:
        secrets_parser = JSONParser("secrets.json")
        db_connection = psycopg2.connect(host=secrets_parser.get_values(['iris_data_source', 'host']),
                                         database=secrets_parser.get_values(['iris_data_source', 'database']),
                                         user=secrets_parser.get_values(['iris_data_source', 'username']),
                                         password=secrets_parser.get_values(['iris_data_source', 'password'])
                                         )
    except Exception as conn_exception:
        print(f'UNABLE TO CONNECT TO DB SERVER\nREASON: {conn_exception}')
        return None
    else:
        print('DB SERVER CONNECTION SUCCESSFUL')
        return db_connection


def read_table_from_database(db_connection, table: str):
    df = None
    if db_connection is not None:
        cursor = db_connection.cursor()
        try:
            cursor.execute(f"SELECT * FROM {table}")
            df = pd.DataFrame(cursor.fetchall())
            df.columns = [col_name[0] for col_name in cursor.description]
        except psycopg2.errors.UndefinedTable as table_err:
            print(table_err)
        cursor.close()
        db_connection.close()
    return df


def save_raw_data():
    db_connection = connect_postgres()
    secrets_parser = JSONParser("secrets.json")
    table = secrets_parser.get_values(['iris_data_source', 'table'])
    if (db_connection is not None) & (table is not None):
        df = read_table_from_database(db_connection, table)
        if df is not None:
            config_parser = JSONParser('config.json')
            raw_data_path = config_parser.get_values(['data_folder', 'raw'])
            df.to_csv(raw_data_path, index=False)
            print('Saved raw file successfully')
        else:
            print("couldn't save raw file")


if __name__ == "__main__":
    save_raw_data()
