import pytest
import pymysql
import psycopg2
from ..constants import DB


class TestDatabase:
    # class: the fixture is destroyed during teardown of the last test in the class.
    @pytest.fixture(scope="class")
    def mysql_client(self, stack_outputs):
        database_username = stack_outputs.get("database_mysql_user").value
        database_password = stack_outputs.get("database_mysql_password").value
        database_name = stack_outputs.get("database_mysql_name").value
        database_port = stack_outputs.get("database_mysql_port").value
        database_host = stack_outputs.get("database_mysql_host").value

        conn = pymysql.connect(
            host=database_host,
            user=database_username,
            password=database_password,
            database=database_name,
            port=database_port,
        )
        yield conn
        # Close connection at the end of tests.
        conn.close()

    # class: the fixture is destroyed during teardown of the last test in the class.
    @pytest.fixture(scope="class")
    def postgresql_client(self, stack_outputs):
        database_username = stack_outputs.get("database_postgresql_user").value
        database_password = stack_outputs.get("database_postgresql_password").value
        database_name = stack_outputs.get("database_postgresql_name").value
        database_port = stack_outputs.get("database_postgresql_port").value
        database_host = stack_outputs.get("database_postgresql_host").value

        conn = psycopg2.connect(
            dbname=database_name,
            user=database_username,
            host=database_host,
            password=database_password,
            port=database_port,
        )
        yield conn
        # Close connection at the end of tests.
        conn.close()

    def test_postgresql_output_name(self, stack_outputs):
        # Test if database name setting is valid.
        database_name = stack_outputs.get("database_postgresql_name").value
        assert DB["POSTGRESQL_NAME"] == database_name

    def test_postgresql_user(self, stack_outputs):
        # Test if database user name setting is valid.
        database_username = stack_outputs.get("database_postgresql_user").value
        assert DB["USER"] == database_username

    def test_mysql_output_name(self, stack_outputs):
        # Test if database name setting is valid.
        database_name = stack_outputs.get("database_mysql_name").value
        assert DB["MYSQL_NAME"] == database_name

    def test_mysql_user(self, stack_outputs):
        # Test if database user name setting is valid.
        database_username = stack_outputs.get("database_mysql_user").value
        assert DB["USER"] == database_username

    def test_mysql_connection(self, mysql_client):
        # Test database connection
        try:
            c = mysql_client.cursor()
            c.execute("SELECT 1")
            connected = True
        except:
            connected = False
        assert connected == True

    def test_postgresql_connection(self, postgresql_client):
        # Test database connection
        try:
            c = postgresql_client.cursor()
            c.execute("SELECT 1")
            connected = True
        except:
            connected = False
        assert connected == True
