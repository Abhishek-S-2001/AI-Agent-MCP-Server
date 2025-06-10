from imports import *
from models.service_category import ServiceCategory

category_bp = Blueprint('category', __name__)

# Get all categories
@category_bp.route("/service-categories", methods=["GET"])
def get_service_categories():
    categories = ServiceCategory.query.all()
    return jsonify([cat.to_dict() for cat in categories])


# Get a category by ID
@category_bp.route("/service-categories/<uuid:category_id>", methods=["GET"])
def get_service_category(category_id):
    category = ServiceCategory.query.get_or_404(category_id)
    return jsonify(category.to_dict())


# Create a new category
@category_bp.route("/service-categories", methods=["POST"])
def create_service_category():
    data = request.get_json()
    if not data.get("category_name"):
        return jsonify({"error": "category_name is required"}), 400

    category = ServiceCategory(category_name=data["category_name"])
    db.session.add(category)
    db.session.commit()
    return jsonify(category.to_dict()), 201


# Update a category
@category_bp.route("/service-categories/<uuid:category_id>", methods=["PUT"])
def update_service_category(category_id):
    category = ServiceCategory.query.get_or_404(category_id)
    data = request.get_json()

    if "category_name" in data:
        category.category_name = data["category_name"]

    db.session.commit()
    return jsonify(category.to_dict())


# Delete a category
@category_bp.route("/service-categories/<uuid:category_id>", methods=["DELETE"])
def delete_service_category(category_id):
    category = ServiceCategory.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted successfully."})
