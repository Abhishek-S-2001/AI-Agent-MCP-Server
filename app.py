from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from config import Config
from db import db
from database.routes.api import api  # your blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    # ✅ Initialize Swagger with default settings
    swagger = Swagger(app, parse=True)

    db.init_app(app)
    app.register_blueprint(api, url_prefix="/api/db")

    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
    "pool_recycle": 280  # seconds
    }
    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=False)
