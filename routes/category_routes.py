from imports import *

category_bp = Blueprint('category', __name__)

@category_bp.route("/service-categories", methods=["GET"])
def get_service_categories():
    categories = ServiceCategory.query.all()
    return jsonify([cat.to_dict() for cat in categories])
