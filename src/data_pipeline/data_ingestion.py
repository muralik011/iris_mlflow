from utils.secrets_parser import SecretsParser
import psycopg2




def connect_postgres():
    try:
        secrets_parser = SecretsParser()
        db_connection = psycopg2.connect(host=secrets_parser.get_values(['data_source', 'host']),
                                         database=secrets_parser.get_values(['data_source', 'database']),
                                         user=secrets_parser.get_values(['data_source', 'username']),
                                         password=secrets_parser.get_values(['data_source', 'username'])
                                         )
    except Exception as conn_exception:
        print(f'UNABLE TO CONNECT TO DB SERVER\nREASON: {conn_exception}')
        return None
    else:
        print('DB SERVER CONNECTION SUCCESSFUL')
        return db_connection
