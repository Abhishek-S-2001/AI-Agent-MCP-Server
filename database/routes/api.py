from imports import *

from database.routes.users_routes import user_bp
from database.routes.provider_routes import provider_bp
from database.routes.category_routes import category_bp
from database.routes.offering_routes import Offering_bp
from database.routes.booking_routes import booking_bp

api = Blueprint('api', __name__)

# Register individual feature routes
api.register_blueprint(user_bp)
api.register_blueprint(provider_bp)
api.register_blueprint(category_bp)
api.register_blueprint(Offering_bp)
api.register_blueprint(booking_bp)
