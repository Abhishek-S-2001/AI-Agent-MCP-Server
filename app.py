from flask import Flask
from flask_cors import CORS
from config import Config
from db import db
from database.routes.api import api

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)

    app.register_blueprint(api, url_prefix="/api/db")

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
