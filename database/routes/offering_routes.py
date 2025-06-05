from imports import *

Offering_bp = Blueprint('offering', __name__)

# GET all offerings
@Offering_bp.route("/offerings", methods=["GET"])
def get_offerings():
    offerings = Offering.query.all()
    return jsonify([o.to_dict() for o in offerings])


# GET offering by ID
@Offering_bp.route("/offerings/<uuid:offering_id>", methods=["GET"])
def get_offering(offering_id):
    offering = Offering.query.get_or_404(offering_id)
    return jsonify(offering.to_dict())


# POST new offering
@Offering_bp.route("/offerings", methods=["POST"])
def create_offering():
    data = request.get_json()
    offering = Offering(offering_name=data["offering_name"])
    db.session.add(offering)
    db.session.commit()
    return jsonify(offering.to_dict()), 201


# PUT to update an offering name
@Offering_bp.route("/offerings/<uuid:offering_id>", methods=["PUT"])
def update_offering(offering_id):
    data = request.get_json()
    offering = Offering.query.get_or_404(offering_id)
    offering.offering_name = data["offering_name"]
    db.session.commit()
    return jsonify(offering.to_dict())


# DELETE offering
@Offering_bp.route("/offerings/<uuid:offering_id>", methods=["DELETE"])
def delete_offering(offering_id):
    offering = Offering.query.get_or_404(offering_id)
    db.session.delete(offering)
    db.session.commit()
    return jsonify({"message": "Offering deleted"})
