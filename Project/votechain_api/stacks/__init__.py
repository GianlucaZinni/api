from flask import Flask
from votechain_api.stacks.auth import AuthStack
from votechain_api.stacks.vote import VoteStack

class Votechain:
    def __init__(self, app: Flask):

        # Initialize the application
        self.app = app
        
        self.auth = AuthStack(app)
        self.vote = VoteStack(app)
