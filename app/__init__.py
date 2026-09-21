from flask import Flask
from app.router.main_router import register_router
from app.middleware import session_data
from app.tables import create_tables
import os

def create_app()->Flask:
    app = Flask(__name__)
    register_router(app)
    app.before_request(session_data)
    os.makedirs(name='app/media',exist_ok=True)
    os.makedirs(name='app/media/importedExcels',exist_ok=True)
    os.makedirs(name='app/media/userQuery',exist_ok=True)
    create_tables()
    return app