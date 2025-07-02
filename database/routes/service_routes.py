from flask import Blueprint, request, jsonify
from database.models.provider_offering import ProviderOffering
from database.models.provider import Provider
from database.models.offering import Offering
from database.models.service_location import ServiceLocation
from database.models.service_type import ServiceType
from sqlalchemy import func
from db import db
from geopy.distance import geodesic

service_bp = Blueprint('services', __name__)

STATIC_USER_LOCATION = (19.0760, 72.8777)  # Example: Mumbai


def extract_city(address):
    if not address:
        return ""
    if "," in address:
        return address.split(",")[-1].strip()
    return address


@service_bp.route("/services", methods=["GET"])
def search_services():
    """
    Search services by service type and/or location with distance from a static user location
    ---
    tags:
      - Services
    parameters:
      - name: type
        in: query
        type: string
        required: false
        description: Filter by service type (e.g., "DNA test")
      - name: location
        in: query
        type: string
        required: false
        description: Filter by location or address
    responses:
      200:
        description: List of matching services with distance
        schema:
          type: object
          properties:
            intent:
              type: string
              example: search_service
            services:
              type: array
              items:
                type: object
                properties:
                  provider_offering_id:
                    type: string
                  provider_name:
                    type: string
                  provider_email:
                    type: string
                  service_name:
                    type: string
                  price:
                    type: number
                  availability_hours:
                    type: string
                  distance_km:
                    type: number
                  location:
                    type: object
                    properties:
                      name:
                        type: string
                      city:
                        type: string
                      latitude:
                        type: number
                      longitude:
                        type: number
    """
    service_type = request.args.get("type", "").lower()
    location = request.args.get("location", "").lower()

    query = db.session.query(
        ProviderOffering.provider_offering_id,
        Provider.company_name.label("provider_name"),
        Provider.email.label("provider_email"),
        Offering.offering_name.label("service_name"),
        Offering.price,
        Offering.availability_hours,
        ServiceLocation.name.label("location_name"),
        ServiceLocation.address,
        ServiceLocation.latitude,
        ServiceLocation.longitude
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
        service_coords = (row.latitude, row.longitude)
        distance_km = geodesic(STATIC_USER_LOCATION, service_coords).km

        services.append({
            "provider_offering_id": row.provider_offering_id,
            "provider_name": row.provider_name,
            "provider_email": row.provider_email,
            "service_name": row.service_name,
            "price": float(row.price) if row.price else None,
            "availability_hours": row.availability_hours,
            "distance_km": round(distance_km, 2),
            "location": {
                "name": row.location_name,
                "city": extract_city(row.address),
                "latitude": row.latitude,
                "longitude": row.longitude
            }
        })

    return jsonify({
        "intent": "search_service",
        "services": services
    })



@service_bp.route("/services/all", methods=["GET"])
def get_all_services():
    """
    Get all available services
    ---
    tags:
      - Services
    responses:
      200:
        description: List of all services
        schema:
          type: object
          properties:
            intent:
              type: string
              example: all_services
            services:
              type: array
              items:
                type: object
                properties:
                  provider_name:
                    type: string
                  provider_email:
                    type: string
                  service_name:
                    type: string
                  price:
                    type: number
                  location:
                    type: object
                    properties:
                      name:
                        type: string
                      address:
                        type: string
    """
    query = db.session.query(
        Provider.company_name.label("provider_name"),
        Provider.email.label("provider_email"),
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
            "provider_email": r.provider_email,
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
    Find services within 5 km of a given location
    ---
    tags:
      - Services
    parameters:
      - name: lat
        in: query
        type: number
        required: true
        description: Latitude
      - name: lon
        in: query
        type: number
        required: true
        description: Longitude
      - name: type
        in: query
        type: string
        required: false
        description: Filter by service type
    responses:
      200:
        description: Services near the specified location
        schema:
          type: object
          properties:
            intent:
              type: string
              example: search_nearby_service
            results:
              type: array
              items:
                type: object
                properties:
                  provider_name:
                    type: string
                  provider_email:
                    type: string
                  service_name:
                    type: string
                  price:
                    type: number
                  availability_hours:
                    type: string
                  location:
                    type: object
                    properties:
                      name:
                        type: string
                      address:
                        type: string
                      latitude:
                        type: number
                      longitude:
                        type: number
                      distance_km:
                        type: number
    """
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    service_type = request.args.get("type", "").lower()

    if lat is None or lon is None:
        return jsonify({"error": "lat and lon are required"}), 400

    query = db.session.query(
        Provider.company_name.label("provider_name"),
        Provider.email.label("provider_email"),
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
                "provider_email": r.provider_email,
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
