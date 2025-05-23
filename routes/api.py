from flask import Blueprint, request, jsonify
from models import Company
from db import db

api = Blueprint('api', __name__)

@api.route("/companies", methods=["GET"])
def get_companies():
    companies = Company.query.all()
    return jsonify([c.to_dict() for c in companies])

@api.route("/companies/<int:id>", methods=["GET"])
def get_company(id):
    company = Company.query.get_or_404(id)
    return jsonify(company.to_dict())

@api.route("/companies", methods=["POST"])
def add_company():
    data = request.get_json()
    company = Company(
        name=data["name"],
        industry=data.get("industry"),
        description=data.get("description")
    )
    db.session.add(company)
    db.session.commit()
    return jsonify(company.to_dict()), 201
