from imports import *
from database.models.provider import Provider
import uuid
from datetime import datetime

provider_bp = Blueprint("provider", __name__)

# GET all providers
@provider_bp.route("/providers", methods=["GET"])
def get_providers():
    providers = Provider.query.all()
    return jsonify([p.to_dict() for p in providers])


# GET single provider by ID
@provider_bp.route("/providers/<uuid:provider_id>", methods=["GET"])
def get_provider(provider_id):
    provider = Provider.query.get_or_404(provider_id)
    return jsonify(provider.to_dict())


# POST create provider
@provider_bp.route("/providers", methods=["POST"])
def create_provider():
    data = request.get_json()

    if not data.get("company_name") or not data.get("license_number"):
        return jsonify({"error": "company_name and license_number are required"}), 400

    provider = Provider(
        provider_id=uuid.uuid4(),
        company_name=data["company_name"],
        license_number=data["license_number"],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(provider)
    db.session.commit()
    return jsonify(provider.to_dict()), 201


# PUT update provider
@provider_bp.route("/providers/<uuid:provider_id>", methods=["PUT"])
def update_provider(provider_id):
    provider = Provider.query.get_or_404(provider_id)
    data = request.get_json()

    if "company_name" in data:
        provider.company_name = data["company_name"]
    if "license_number" in data:
        provider.license_number = data["license_number"]

    provider.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(provider.to_dict())


# DELETE provider
@provider_bp.route("/providers/<uuid:provider_id>", methods=["DELETE"])
def delete_provider(provider_id):
    provider = Provider.query.get_or_404(provider_id)
    db.session.delete(provider)
    db.session.commit()
    return jsonify({"message": "Provider deleted successfully."})
