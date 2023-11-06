from flask import Flask

class SignatureStack:
    def __init__(self, app: Flask):
        self.app = app