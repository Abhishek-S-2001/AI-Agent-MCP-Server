from imports import *

from database.routes.users_routes import user_bp
from database.routes.provider_routes import provider_bp
from database.routes.category_routes import category_bp
from database.routes.offering_routes import offering_bp
from database.routes.booking_routes import booking_bp
from database.routes.service_routes import service_bp
from database.routes.ai_agent_routes import ai_bp
from database.routes.ai_provider_agent_routes import provider_ai_bp


api = Blueprint('api', __name__)

# Register individual feature routes
api.register_blueprint(ai_bp)
api.register_blueprint(provider_ai_bp)

api.register_blueprint(user_bp)
api.register_blueprint(provider_bp)
api.register_blueprint(category_bp)
api.register_blueprint(offering_bp)
api.register_blueprint(service_bp)
api.register_blueprint(booking_bp)
