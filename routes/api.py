from imports import *

from routes.category_routes import category_bp
from routes.offering_routes import Offering_bp

api = Blueprint('api', __name__)

# Register individual feature routes
api.register_blueprint(category_bp)
api.register_blueprint(Offering_bp)
