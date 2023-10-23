from database.mysql_handler import MySQLDatabaseHandler


def create_table(
    table_name,
    partition_key,
    sort_key=None,
    attributes: list = None,
    ttl_attribute=None,
):
    db = MySQLDatabaseHandler()
    check_tables = db.get_tables(table_name)
    if not table_name in check_tables:
        # Define la estructura de la tabla en SQL
        create_table_query = f"""
            CREATE TABLE {table_name} (
                {partition_key} VARCHAR(255) PRIMARY KEY,
            """
        if sort_key:
            create_table_query += f"{sort_key} VARCHAR(255),"

        if ttl_attribute:
            create_table_query += f"{ttl_attribute} DATETIME,"

        if attributes:
            for name in attributes:
                create_table_query += f"{name} VARCHAR(255),"

        if create_table_query.endswith(","):
            create_table_query = create_table_query[:-1]

        create_table_query += ");"

        db.query(create_table_query)
