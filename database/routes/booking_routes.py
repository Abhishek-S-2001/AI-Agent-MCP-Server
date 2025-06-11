from imports import *
from database.models.booking import Booking
import uuid

booking_bp = Blueprint("booking", __name__)

# GET all bookings
@booking_bp.route("/bookings", methods=["GET"])
def get_bookings():
    bookings = Booking.query.all()
    return jsonify([b.to_dict() for b in bookings])


# GET single booking
@booking_bp.route("/bookings/<uuid:booking_id>", methods=["GET"])
def get_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return jsonify(booking.to_dict())


# POST create a new booking
@booking_bp.route("/bookings", methods=["POST"])
def create_booking():
    data = request.get_json()
    booking = Booking(
        booking_id=uuid.uuid4(),
        service_offering_id=data["service_offering_id"],
        appointment_date=data.get("appointment_date"),
        appointment_start_time=data.get("appointment_start_time"),
        appointment_end_time=data.get("appointment_end_time"),
        status=data.get("status", "pending"),
        notes=data.get("notes"),
        user_id=data["user_id"],
        provider_id=data["provider_id"]
    )
    db.session.add(booking)
    db.session.commit()
    return jsonify(booking.to_dict()), 201


# PUT update booking
@booking_bp.route("/bookings/<uuid:booking_id>", methods=["PUT"])
def update_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    data = request.get_json()

    booking.service_offering_id = data.get("service_offering_id", booking.service_offering_id)
    booking.appointment_date = data.get("appointment_date", booking.appointment_date)
    booking.appointment_start_time = data.get("appointment_start_time", booking.appointment_start_time)
    booking.appointment_end_time = data.get("appointment_end_time", booking.appointment_end_time)
    booking.status = data.get("status", booking.status)
    booking.notes = data.get("notes", booking.notes)
    booking.user_id = data.get("user_id", booking.user_id)
    booking.provider_id = data.get("provider_id", booking.provider_id)

    db.session.commit()
    return jsonify(booking.to_dict())


# DELETE booking
@booking_bp.route("/bookings/<uuid:booking_id>", methods=["DELETE"])
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    return jsonify({"message": "Booking deleted successfully."})
