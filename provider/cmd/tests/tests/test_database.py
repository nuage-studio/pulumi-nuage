from io import StringIO
import pytest
import pymysql
import psycopg2
import paramiko
from sshtunnel import SSHTunnelForwarder
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

        # Get bastion config
        bastion_ip = stack_outputs.get("database_postgresql_bastion_ip").value
        bastion_private_key = stack_outputs.get("database_postgresql_bastion_private_key").value

        keyfile = StringIO(bastion_private_key)
        pkey = paramiko.RSAKey.from_private_key(keyfile)

        tunnel = SSHTunnelForwarder(
            bastion_ip,
            ssh_username="ubuntu",
            ssh_pkey=pkey,
            remote_bind_address=(database_host, database_port),
            local_bind_address=("127.0.0.1", database_port),
        )

        tunnel.start()
        conn = psycopg2.connect(
            dbname=database_name,
            user=database_username,
            password=database_password,
            host=tunnel.local_bind_host,
            port=tunnel.local_bind_port,
        )
        yield conn
        # Close connection at the end of tests.
        conn.close()
        tunnel.stop()

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
