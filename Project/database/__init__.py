from resources import IntegratorResources


class DatabaseStack:
    def __init__(self):

        resources = IntegratorResources()

        self.enviroment_variables = {
            "DB_CONFIG": resources.params["DB_CONFIG"],
            "SQLALCHEMY_DATABASE_URI": resources.params["DB_CONFIG"]["SQLALCHEMY"]["DATABASE_URI"],
        }

db_app = DatabaseStack()