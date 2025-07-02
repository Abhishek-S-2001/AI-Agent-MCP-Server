from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from config import Config
from db import db
from database.routes.api import api  # your blueprint
import os

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

    @app.route("/")
    def index():
        return "Flask app is running!"

    return app

app = create_app()

if __name__ == "__main__":
    # ✅ Bind to 0.0.0.0 and pick up the correct port from environment
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
