from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    
    app.config['DATA_DIR'] = os.path.join(os.path.dirname(__file__), '..', 'data')
    app.config['INVENTORY_FILE'] = 'current_inventory.txt'

    from app.routes import register_routes
    register_routes(app)

    return app