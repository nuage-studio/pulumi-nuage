import pymysql
import psycopg2
from constants import DB


class TestsDB:
    def test_postgresql_output_name(self):
        # Test if database name setting is valid.
        database_name = self.outputs.get("database_postgresql_name").value
        self.assertEqual(DB["POSTGRESQL_NAME"], database_name)

    def test_postgresql_user(self):
        # Test if database user name setting is valid.
        database_username = self.outputs.get("database_postgresql_user").value
        self.assertEqual(DB["USER"], database_username)

    def test_mysql_output_name(self):
        # Test if database name setting is valid.
        database_name = self.outputs.get("database_mysql_name").value
        self.assertEqual(DB["MYSQL_NAME"], database_name)

    def test_mysql_user(self):
        # Test if database user name setting is valid.
        database_username = self.outputs.get("database_mysql_user").value
        self.assertEqual(DB["USER"], database_username)

    def test_mysql_connection(self):
        # Test database connection
        database_username = self.outputs.get("database_mysql_user").value
        database_password = self.outputs.get("database_mysql_password").value
        database_name = self.outputs.get("database_mysql_name").value
        database_port = self.outputs.get("database_mysql_port").value
        database_host = self.outputs.get("database_mysql_host").value

        connected = False
        try:
            conn = pymysql.connect(
                host=database_host,
                user=database_username,
                password=database_password,
                database=database_name,
                port=database_port,
            )
            c = conn.cursor()
            c.execute("SELECT 1")
            conn.close()
            connected = True
        except:
            pass
        self.assertEqual(connected, True)

    def test_postgresql_connection(self):
        # Test database connection
        database_username = self.outputs.get("database_postgresql_user").value
        database_password = self.outputs.get("database_postgresql_password").value
        database_name = self.outputs.get("database_postgresql_name").value
        database_port = self.outputs.get("database_postgresql_port").value
        database_host = self.outputs.get("database_postgresql_host").value

        connected = False
        try:
            conn = psycopg2.connect(
                dbname=database_name,
                user=database_username,
                host=database_host,
                password=database_password,
                port=database_port,
            )
            c = conn.cursor()
            c.execute("SELECT 1")
            conn.close()
            connected = True
        except:
            pass
        self.assertEqual(connected, True)
