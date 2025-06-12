from imports import *
from database.models.service_category import ServiceCategory
import uuid
from datetime import datetime

category_bp = Blueprint('category', __name__)

# GET all categories
@category_bp.route("/service-categories", methods=["GET"])
def get_service_categories():
    categories = ServiceCategory.query.all()
    return jsonify([cat.to_dict() for cat in categories])


# GET a specific category
@category_bp.route("/service-categories/<uuid:category_id>", methods=["GET"])
def get_service_category(category_id):
    category = ServiceCategory.query.get_or_404(category_id)
    return jsonify(category.to_dict())


# POST create a new category
@category_bp.route("/service-categories", methods=["POST"])
def create_service_category():
    data = request.get_json()
    name = data.get("category_name")

    if not name:
        return jsonify({"error": "category_name is required"}), 400

    category = ServiceCategory(
        category_name=name,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(category)
    db.session.commit()
    return jsonify(category.to_dict()), 201


# PUT update an existing category
@category_bp.route("/service-categories/<uuid:category_id>", methods=["PUT"])
def update_service_category(category_id):
    category = ServiceCategory.query.get_or_404(category_id)
    data = request.get_json()

    if "category_name" in data:
        category.category_name = data["category_name"]
        category.updated_at = datetime.utcnow()

    db.session.commit()
    return jsonify(category.to_dict())


# DELETE a category
@category_bp.route("/service-categories/<uuid:category_id>", methods=["DELETE"])
def delete_service_category(category_id):
    category = ServiceCategory.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted successfully."})
