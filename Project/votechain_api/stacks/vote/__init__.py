from flask import Flask
from database.mysql.index import MySQLHandler
from database.sqlalchemy.index import SQLAlchemyHandler


class VoteStack:
    def __init__(self, app: Flask = None):
        
        # SQLAlchemy Handler
        self.sqlalchemy = SQLAlchemyHandler()
        self.db_session = self.sqlalchemy.connect("VOTECHAIN")


# Create Votechain database connection
mysql_votechain = MySQLHandler("VOTECHAIN")

vote_auditory = mysql_votechain.create_table(
    table_name="vote_auditory",
    partition_key="DNI",
    attributes=["audit", "timestamp"],
)

email_verification = mysql_votechain.create_table(
    table_name="email_verification",
    partition_key="code",
    attributes=["expiration_time", "google_id"],
)

mysql_renaper = MySQLHandler("RENAPER")
individuos = mysql_renaper.create_table(
    table_name="individuos",
    partition_key="DNI",
    sort_key="email",
    attributes=[
        "telefono",
    ],
)
