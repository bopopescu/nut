from flask import Flask
from flask_cli import FlaskCLI
from model.base import db

app = Flask(__name__)
FlaskCLI(app)

def init_db():
    db.create_all()

@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')

