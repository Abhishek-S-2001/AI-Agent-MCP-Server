from imports import *
from database.models.provider import Provider
import uuid

provider_bp = Blueprint("provider", __name__)

# GET all providers
@provider_bp.route("/providers", methods=["GET"])
def get_providers():
    providers = Provider.query.all()
    return jsonify([p.to_dict() for p in providers])


# GET single provider
@provider_bp.route("/providers/<uuid:provider_id>", methods=["GET"])
def get_provider(provider_id):
    provider = Provider.query.get_or_404(provider_id)
    return jsonify(provider.to_dict())


# POST create provider
@provider_bp.route("/providers", methods=["POST"])
def create_provider():
    data = request.get_json()

    provider = Provider(
        provider_id=uuid.uuid4(),  # or use data["provider_id"] if given explicitly
        company_name=data.get("company_name"),
        license_number=data.get("license_number"),
        address=data.get("address")
    )
    db.session.add(provider)
    db.session.commit()
    return jsonify(provider.to_dict()), 201


# PUT update provider
@provider_bp.route("/providers/<uuid:provider_id>", methods=["PUT"])
def update_provider(provider_id):
    provider = Provider.query.get_or_404(provider_id)
    data = request.get_json()

    provider.company_name = data.get("company_name", provider.company_name)
    provider.license_number = data.get("license_number", provider.license_number)
    provider.address = data.get("address", provider.address)

    db.session.commit()
    return jsonify(provider.to_dict())


# DELETE provider
@provider_bp.route("/providers/<uuid:provider_id>", methods=["DELETE"])
def delete_provider(provider_id):
    provider = Provider.query.get_or_404(provider_id)
    db.session.delete(provider)
    db.session.commit()
    return jsonify({"message": "Provider deleted successfully."})
