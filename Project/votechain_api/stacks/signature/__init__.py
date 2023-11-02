from flask import Flask
from layers.database.functions.mysql_handler import MySQLDatabaseHandler

class SignatureStack:
    def __init__(self, app: Flask):
        self.app = app
        self.db = MySQLDatabaseHandler(database_name="SignaturesDB")

        self.signature_keys = self.db.create_table(
            id="signature_keys",
            partition_key="id",
            attributes=["public_key", "private_key"]
        )