import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class DB:
    def __init__(self, host: str, user: str, password: str, database: str):
        try:
            self.connection = psycopg2.connect(host=host,
                                               user=user,
                                               password=password,
                                               database=database
                                               )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        except (Exception, Error) as error:
            print(error)

    def create_database(self, database_name: str):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f'CREATE DATABASE {database_name}')
                self.connection.commit()
                return None
        except (Exception, Error) as error:
            return print(error)

    def create_table(self, table_name: str, params: str):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"CREATE TABLE {table_name}({params});")
                self.connection.commit()
                return None
        except (Exception, Error) as error:
            return print(error)

    async def insert_into(self, table_name: str, columns: str, params: str | int):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({params});")
                self.connection.commit()
                return None
        except (Exception, Error) as error:
            return print(error)

    async def select_fetchone(self, table_name: str, colum: str, param: str | int = None, value: str | int = None):
        try:
            with self.connection.cursor() as cursor:
                if value is None:
                    cursor.execute(f"SELECT {colum} FROM {table_name}")
                if value is not None:
                    cursor.execute(f"SELECT {colum} FROM {table_name} WHERE {param} = {value}")
                return cursor.fetchone()
        except (Exception, Error) as error:
            return print(error)

    async def select_fetchall(self, table_name: str, colum: str, param: str | int = None, value: str | int = None):
        try:
            with self.connection.cursor() as cursor:
                if value is None:
                    cursor.execute(f"SELECT {colum} FROM {table_name}")
                if value is not None:
                    cursor.execute(f"SELECT {colum} FROM {table_name} WHERE {param} = {value}")
                return cursor.fetchall()
        except (Exception, Error) as error:
            return print(error)

    async def delete(self, table_name: str, colum: str = None, param: str | int = None, value: str | int = None):
        try:
            with self.connection.cursor() as cursor:
                if value is None:
                    pass
                # cursor.execute(f"DELETE FROM {table_name} * ")
                if value is not None:
                    cursor.execute(f"DELETE {colum} FROM {table_name} WHERE {param} = {value}")
                self.connection.commit()
                return None
        except (Exception, Error) as error:
            return print(error)


    async def update(self, table_name: str, colum: str, colum_value: str | int, param: str | int, value: str | int):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"UPDATE {table_name} SET {colum}={colum_value} WHERE {param} = {value}")
                self.connection.commit()
                return None
        except (Exception, Error) as error:
            return print(error)
