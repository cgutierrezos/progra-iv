import unittest
from environment import Environment, FakeEnvironment

from src.providers.MySQLProvider import MySQLProvider




class TestMySQLProvider(unittest.TestCase):
        

    @classmethod
    def setUpClass(cls):
        # Se ejecuta una vez antes de todas las pruebas
        cls.env: Environment = FakeEnvironment({"MYSQL_HOST": "localhost", "MYSQL_PORT": "3306", "MYSQL_DB": "test_progra4", "MYSQL_USER": "test_progra4", "MYSQL_PASS": ""})
        cls.mysqlProvider = MySQLProvider(cls.env)
        cls.mysqlProvider.connect()


    def setUp(self):
        self.mysqlProvider.execute("SET FOREIGN_KEY_CHECKS = 0")
        self.mysqlProvider.execute("TRUNCATE TABLE customers")
        self.mysqlProvider.execute("SET FOREIGN_KEY_CHECKS = 1")
        
    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        # Se ejecuta una vez después de todas las pruebas
        cls.mysqlProvider.execute("SET FOREIGN_KEY_CHECKS = 0")
        cls.mysqlProvider.execute("TRUNCATE TABLE customers")
        cls.mysqlProvider.execute("SET FOREIGN_KEY_CHECKS = 1")
        cls.mysqlProvider.disconnect()
    

    def test_create_customer(self):
        """
        Test that it can insert a customer id mysql db
        """

        id = "1"
        name = "cristian"
        identification = "1088018783"

        self.mysqlProvider.execute(f"INSERT INTO customers (id, name, identification) VALUES ('{id}', '{name}', '{identification}')")

        fetch = self.mysqlProvider.fetch(f"SELECT id, name, identification FROM customers WHERE id = '{id}' LIMIT 1")

        self.assertEqual(len(fetch), 1)

        row = fetch[0]

        self.assertEqual(str(row[0]), id)
        self.assertEqual(str(row[1]), name)
        self.assertEqual(str(row[2]), identification)

        


    def test_update_customer(self):
        """
        Test that it can UPDATE a customer id mysql db
        """

        id = "1"
        name = "cristian"
        identification = "1088018783"

        self.mysqlProvider.execute(f"INSERT INTO customers (id, name, identification) VALUES ('{id}', '{name}', '{identification}')")

        fetch = self.mysqlProvider.fetch(f"SELECT id, name, identification FROM customers WHERE id = '{id}' LIMIT 1")

        self.assertEqual(len(fetch), 1)

        row = fetch[0]

        self.assertEqual(str(row[0]), id)
        self.assertEqual(str(row[1]), name)
        self.assertEqual(str(row[2]), identification)

        newName = "alejandro"
        self.mysqlProvider.execute(f"UPDATE customers SET name='{newName}' WHERE id = '{id}' LIMIT 1")

        fetch = self.mysqlProvider.fetch(f"SELECT id, name, identification FROM customers WHERE id = '{id}' LIMIT 1")

        self.assertEqual(len(fetch), 1)

        row = fetch[0]

        self.assertEqual(str(row[0]), id)
        self.assertEqual(str(row[1]), newName)
        self.assertEqual(str(row[2]), identification)


    def test_delete_customer(self):
        """
        Test that it can DELETE a customer id mysql db
        """

        id = "1"
        name = "cristian"
        identification = "1088018783"

        self.mysqlProvider.execute(f"INSERT INTO customers (id, name, identification) VALUES ('{id}', '{name}', '{identification}')")

        fetch = self.mysqlProvider.fetch(f"SELECT id, name, identification FROM customers WHERE id = '{id}' LIMIT 1")

        self.assertEqual(len(fetch), 1)

        row = fetch[0]

        self.assertEqual(str(row[0]), id)
        self.assertEqual(str(row[1]), name)
        self.assertEqual(str(row[2]), identification)

        
        self.mysqlProvider.execute(f"DELETE FROM customers WHERE id = '{id}' LIMIT 1")

        fetch = self.mysqlProvider.fetch(f"SELECT id, name, identification FROM customers WHERE id = '{id}' LIMIT 1")

        self.assertEqual(len(fetch), 0)
       
        
