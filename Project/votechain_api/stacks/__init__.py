from flask import Flask
from votechain_api.stacks.auth import AuthStack

class Votechain:
    def __init__(self, app: Flask):

        # Initialize the application
        self.app = app
        
        self.auth = AuthStack(app)
