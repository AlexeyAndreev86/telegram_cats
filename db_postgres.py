import psycopg2
import yaml


class DB:
    def read_config(self):
        with open('config.yml') as f:
            setup = yaml.load(f, Loader=yaml.FullLoader)
        return setup

    def __init__(self):
        setup = self.read_config()
        self.connection = psycopg2.connect(user=setup['user'],
                                           password=setup['password'],
                                           host=setup['host'],
                                           port=setup['port'],
                                           database=setup['database'])
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.cursor.close()
        self.connection.close()
