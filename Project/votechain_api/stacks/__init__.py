from flask import Flask
from votechain_api.stacks.api import ApiStack
from votechain_api.stacks.controller import ControllerStack


class Votechain:
    def __init__(self, app: Flask):
        # Initialize the application
        self.app = app

        self.api = ApiStack(app)
        self.controller = ControllerStack(app)
