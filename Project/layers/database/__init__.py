from layers.resources import IntegratorResources


class DatabaseStack:
    def __init__(self):

        resources = IntegratorResources()

        self.enviroment_variables = ""

db_app = DatabaseStack()