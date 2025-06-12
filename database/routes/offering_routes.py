from imports import *
from database.models.offering import Offering
import uuid
from datetime import datetime

offering_bp = Blueprint('offering', __name__)

# GET all offerings
@offering_bp.route("/offerings", methods=["GET"])
def get_offerings():
    offerings = Offering.query.all()
    return jsonify([o.to_dict() for o in offerings])


# GET single offering by ID
@offering_bp.route("/offerings/<uuid:offering_id>", methods=["GET"])
def get_offering(offering_id):
    offering = Offering.query.get_or_404(offering_id)
    return jsonify(offering.to_dict())


# POST create new offering
@offering_bp.route("/offerings", methods=["POST"])
def create_offering():
    data = request.get_json()
    if "offering_name" not in data:
        return jsonify({"error": "offering_name is required"}), 400

    offering = Offering(
        offering_name=data["offering_name"],
        price=data.get("price"),
        availability_hours=data.get("availability_hours"),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(offering)
    db.session.commit()
    return jsonify(offering.to_dict()), 201


# PUT update offering
@offering_bp.route("/offerings/<uuid:offering_id>", methods=["PUT"])
def update_offering(offering_id):
    offering = Offering.query.get_or_404(offering_id)
    data = request.get_json()

    if "offering_name" in data:
        offering.offering_name = data["offering_name"]
    if "price" in data:
        offering.price = data["price"]
    if "availability_hours" in data:
        offering.availability_hours = data["availability_hours"]

    offering.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(offering.to_dict())


# DELETE offering
@offering_bp.route("/offerings/<uuid:offering_id>", methods=["DELETE"])
def delete_offering(offering_id):
    offering = Offering.query.get_or_404(offering_id)
    db.session.delete(offering)
    db.session.commit()
    return jsonify({"message": "Offering deleted"})
