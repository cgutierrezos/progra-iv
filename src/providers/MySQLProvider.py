from typing import Any, List
from environment import Environment
from mysql import connector

class MySQLProvider:

    def __init__(self, env: Environment) -> None:
        self.MYSQL_HOST = env.getOrFails("MYSQL_HOST")
        self.MYSQL_PORT = env.getOrFails("MYSQL_PORT")
        self.MYSQL_DB = env.getOrFails("MYSQL_DB")
        self.MYSQL_USER = env.getOrFails("MYSQL_USER")
        self.MYSQL_PASS = env.getOrFails("MYSQL_PASS")
        self.connection: connector.pooling.PooledMySQLConnection | connector.pooling.MySQLConnectionAbstract
        self.cursor: connector.connection.MySQLCursor | Any


    def connect(self):
        self.connection = connector.connect(
            host=self.MYSQL_HOST, 
            port=self.MYSQL_PORT, 
            database=self.MYSQL_DB, 
            user=self.MYSQL_USER, 
            password=self.MYSQL_PASS
        )

        self.cursor = self.connection.cursor()


    def execute(self, sql: str):
        self.cursor.execute(sql)
        self.connection.commit()

    def fetch(self, sql: str) -> List[connector.connection.RowType] | Any:
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def disconnect(self):
        self.cursor.close()
        self.connection.close()