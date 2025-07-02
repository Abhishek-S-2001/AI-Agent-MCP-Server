from flask import Blueprint, request, jsonify
from db import db
from sqlalchemy import func
from database.models.provider import Provider
from database.models.offering import Offering
from database.models.provider_offering import ProviderOffering
from database.models.service_location import ServiceLocation
from database.models.booking import Booking
from database.models.users import User

import uuid
from datetime import datetime
from geopy.distance import geodesic

ai_bp = Blueprint("ai_agent", __name__)


@ai_bp.route("/ai/services", methods=["GET"])
def ai_search_services():
    """
    Search services by offering type and location
    ---
    parameters:
      - name: type
        in: query
        type: string
        required: false
      - name: location
        in: query
        type: string
        required: false
    """
    service_type = request.args.get("type", "").lower()
    location = request.args.get("location", "").lower()

    query = db.session.query(
        Provider.company_name.label("provider_name"),
        Offering.offering_name,
        Offering.price,
        Offering.availability_hours,
        ServiceLocation.name.label("location_name"),
        ServiceLocation.address,
        ProviderOffering.provider_offering_id
    ).join(
        ProviderOffering, Provider.provider_id == ProviderOffering.provider_id
    ).join(
        Offering, Offering.offering_id == ProviderOffering.offering_id
    ).join(
        ServiceLocation, ServiceLocation.location_id == ProviderOffering.location_id
    )

    if service_type:
        query = query.filter(func.lower(Offering.offering_name).like(f"%{service_type}%"))
    if location:
        query = query.filter(
            func.lower(ServiceLocation.name).like(f"%{location}%") |
            func.lower(ServiceLocation.address).like(f"%{location}%")
        )

    results = query.all()

    return jsonify({
        "services": [
            {
                "provider_offering_id": row.provider_offering_id,
                "provider_name": row.provider_name,
                "service_name": row.offering_name,
                "price": float(row.price),
                "availability_hours": row.availability_hours,
                "location": {
                    "name": row.location_name,
                    "address": row.address
                }
            }
            for row in results
        ]
    })


@ai_bp.route("/ai/book", methods=["POST"])
def ai_book_appointment():
    """
    Book an appointment
    ---
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              user_id:
                type: string
              provider_offering_id:
                type: string
              appointment_date:
                type: string
              appointment_start_time:
                type: string
              appointment_end_time:
                type: string
              notes:
                type: string
    responses:
      200:
        description: Booking created
    """
    data = request.get_json()

    booking = Booking(
        booking_id=str(uuid.uuid4()),
        provider_offering_id=data["provider_offering_id"],
        user_id=data["user_id"],
        booking_time=datetime.utcnow(),
        appointment_date=data["appointment_date"],
        appointment_start_time=data["appointment_start_time"],
        appointment_end_time=data["appointment_end_time"],
        notes=data.get("notes", ""),
        status="Pending"
    )
    db.session.add(booking)
    db.session.commit()

    return jsonify({"message": "Booking created", "booking_id": booking.booking_id})


@ai_bp.route("/ai/bookings", methods=["GET"])
def ai_list_all_bookings():
    """
    List all bookings (admin)
    """
    query = db.session.query(
        Booking.booking_id,
        Booking.appointment_date,
        Booking.appointment_start_time,
        Booking.appointment_end_time,
        Booking.status,
        Booking.notes,
        User.name.label("user_name"),
        Provider.company_name.label("provider_name"),
        Offering.offering_name.label("service_name"),
        ServiceLocation.name.label("location_name")
    ).join(
        User, Booking.user_id == User.user_id
    ).join(
        ProviderOffering, ProviderOffering.provider_offering_id == Booking.provider_offering_id
    ).join(
        Provider, Provider.provider_id == ProviderOffering.provider_id
    ).join(
        Offering, Offering.offering_id == ProviderOffering.offering_id
    ).join(
        ServiceLocation, ServiceLocation.location_id == ProviderOffering.location_id
    )

    results = query.all()

    return jsonify([{
        "booking_id": row.booking_id,
        "user_name": row.user_name,
        "provider_name": row.provider_name,
        "service_name": row.service_name,
        "location": row.location_name,
        "date": str(row.appointment_date),
        "start": str(row.appointment_start_time),
        "end": str(row.appointment_end_time),
        "status": row.status,
        "notes": row.notes
    } for row in results])


@ai_bp.route("/ai/bookings/<user_id>", methods=["GET"])
def ai_user_bookings(user_id):
    """
    List bookings for a specific user
    """
    query = db.session.query(
        Booking.booking_id,
        Booking.appointment_date,
        Booking.appointment_start_time,
        Booking.appointment_end_time,
        Booking.status,
        Booking.notes,
        Provider.company_name.label("provider_name"),
        Offering.offering_name.label("service_name"),
        ServiceLocation.name.label("location_name")
    ).join(
        ProviderOffering, ProviderOffering.provider_offering_id == Booking.provider_offering_id
    ).join(
        Provider, Provider.provider_id == ProviderOffering.provider_id
    ).join(
        Offering, Offering.offering_id == ProviderOffering.offering_id
    ).join(
        ServiceLocation, ServiceLocation.location_id == ProviderOffering.location_id
    ).filter(
        Booking.user_id == user_id
    )

    results = query.all()

    return jsonify([{
        "booking_id": row.booking_id,
        "provider_name": row.provider_name,
        "service_name": row.service_name,
        "location": row.location_name,
        "date": str(row.appointment_date),
        "start": str(row.appointment_start_time),
        "end": str(row.appointment_end_time),
        "status": row.status,
        "notes": row.notes
    } for row in results])
