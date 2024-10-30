# app/__init__.py
from flask import Flask

from app.Route.General_route import general_bp
from app.Route.User_route import user_bp
from app.Route.Printer_Owner_route import puser_bp
from app.Route.Print_req_route import print_req_bp
def create_app():
    app = Flask(__name__)
    from flask_cors import CORS
    CORS(app)
    app.secret_key = 'Dheeraj@2006'
    app.register_blueprint(general_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(puser_bp)
    app.register_blueprint(print_req_bp)
    # Other app configuration and setup here
    return app