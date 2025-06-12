from imports import *

from database.models.provider_offering import ProviderOffering
from database.models.provider import Provider
from database.models.offering import Offering
from database.models.service_location import ServiceLocation
from database.models.service_type import ServiceType
from sqlalchemy import func
from db import db
from geopy.distance import geodesic

service_bp = Blueprint('services', __name__)


def extract_city(address):
    """
    Extracts the city part from an address string.
    Assumes the last comma-separated token is the city.
    """
    if not address:
        return ""
    if "," in address:
        return address.split(",")[-1].strip()
    return address


@service_bp.route("/services", methods=["GET"])
def search_services():
    """
    Search services by service type and/or location.
    Query Parameters:
    - type: Filter by service type (e.g., "DNA test")
    - location: Filter by location name or city (e.g., "Andheri")
    """
    service_type = request.args.get("type", "").lower()
    location = request.args.get("location", "").lower()

    query = db.session.query(
        Provider.company_name.label("provider_name"),
        Offering.offering_name.label("service_name"),
        Offering.price,
        ServiceLocation.name.label("location_name"),
        ServiceLocation.address,
    ).join(
        ProviderOffering, ProviderOffering.provider_id == Provider.provider_id
    ).join(
        Offering, Offering.offering_id == ProviderOffering.offering_id
    ).join(
        ServiceLocation, ServiceLocation.location_id == ProviderOffering.location_id
    ).join(
        ServiceType, ServiceType.type_id == ServiceLocation.type_id
    )

    if service_type:
        query = query.filter(func.lower(ServiceType.type_name).like(f"%{service_type}%"))

    if location:
        query = query.filter(
            func.lower(ServiceLocation.name).like(f"%{location}%") |
            func.lower(ServiceLocation.address).like(f"%{location}%")
        )

    results = query.all()

    services = []
    for row in results:
        services.append({
            "provider_name": row.provider_name,
            "service_name": row.service_name,
            "price": float(row.price) if row.price else None,
            "location": {
                "name": row.location_name,
                "city": extract_city(row.address)
            }
        })

    return jsonify({
        "intent": "search_service",
        "services": services
    })


@service_bp.route("/services/all", methods=["GET"])
def get_all_services():
    """
    Get all services available in the system without any filters.
    """
    query = db.session.query(
        Provider.company_name.label("provider_name"),
        Offering.offering_name.label("service_name"),
        Offering.price,
        ServiceLocation.name.label("location_name"),
        ServiceLocation.address
    ).join(
        ProviderOffering, ProviderOffering.provider_id == Provider.provider_id
    ).join(
        Offering, Offering.offering_id == ProviderOffering.offering_id
    ).join(
        ServiceLocation, ServiceLocation.location_id == ProviderOffering.location_id
    )

    results = query.all()

    services = []
    for r in results:
        services.append({
            "provider_name": r.provider_name,
            "service_name": r.service_name,
            "price": float(r.price),
            "location": {
                "name": r.location_name,
                "address": r.address
            }
        })

    return jsonify({
        "intent": "all_services",
        "services": services
    })


@service_bp.route("/services/nearby", methods=["GET"])
def get_nearby_services():
    """
    Find services within 5 km of given lat/lon.
    Query Parameters:
    - lat: Latitude (required)
    - lon: Longitude (required)
    - type: Optional filter for service type
    """
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    service_type = request.args.get("type", "").lower()

    if lat is None or lon is None:
        return jsonify({"error": "lat and lon are required"}), 400

    query = db.session.query(
        Provider.company_name.label("provider_name"),
        Offering.offering_name.label("service_name"),
        Offering.price,
        Offering.availability_hours,
        ServiceLocation.name.label("location_name"),
        ServiceLocation.latitude,
        ServiceLocation.longitude,
        ServiceLocation.address
    ).join(
        ProviderOffering, ProviderOffering.provider_id == Provider.provider_id
    ).join(
        Offering, Offering.offering_id == ProviderOffering.offering_id
    ).join(
        ServiceLocation, ServiceLocation.location_id == ProviderOffering.location_id
    )

    if service_type:
        query = query.filter(func.lower(Offering.offering_name).like(f"%{service_type}%"))

    all_results = query.all()

    user_location = (lat, lon)
    nearby_services = []

    for r in all_results:
        location_coords = (r.latitude, r.longitude)
        distance_km = geodesic(user_location, location_coords).km
        if distance_km <= 5:
            nearby_services.append({
                "provider_name": r.provider_name,
                "service_name": r.service_name,
                "price": float(r.price),
                "availability_hours": r.availability_hours,
                "location": {
                    "name": r.location_name,
                    "address": r.address,
                    "latitude": r.latitude,
                    "longitude": r.longitude,
                    "distance_km": round(distance_km, 2)
                }
            })

    return jsonify({
        "intent": "search_nearby_service",
        "results": nearby_services
    })
