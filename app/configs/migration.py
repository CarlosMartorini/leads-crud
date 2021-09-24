from flask import Flask
from flask_migrate import Migrate

def init_app(app: Flask):
    
    # TODO: from ... import ...

    Migrate(app, app.db)