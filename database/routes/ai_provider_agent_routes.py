from flask import Blueprint, request, jsonify
from db import db
from database.models.booking import Booking
from database.models.users import User
from database.models.provider import Provider
from database.models.offering import Offering
from database.models.service_location import ServiceLocation
from database.models.provider_offering import ProviderOffering
from database.models.conversation import Conversation
from datetime import datetime
from sqlalchemy import func
import uuid

provider_ai_bp = Blueprint("ai_provider_agent", __name__)


@provider_ai_bp.route("/ai/provider/<provider_id>/bookings", methods=["GET"])
def provider_bookings(provider_id):
    """
    View Bookings for a Provider
    ---
    tags:
      - Provider AI Agent
    parameters:
      - name: provider_id
        in: path
        required: true
        type: string
        description: UUID of the provider
    responses:
      200:
        description: List of bookings for the provider
        schema:
          type: array
          items:
            type: object
            properties:
              booking_id:
                type: string
              status:
                type: string
              appointment_date:
                type: string
              start_time:
                type: string
              end_time:
                type: string
              notes:
                type: string
              user:
                type: object
                properties:
                  name: {type: string}
                  email: {type: string}
              service:
                type: string
              location:
                type: string
    """
    query = db.session.query(
        Booking.booking_id,
        Booking.status,
        Booking.appointment_date,
        Booking.appointment_start_time,
        Booking.appointment_end_time,
        Booking.notes,
        User.name.label("user_name"),
        User.email.label("user_email"),
        Offering.offering_name.label("service_name"),
        ServiceLocation.name.label("location_name")
    ).join(
        User, Booking.user_id == User.user_id
    ).join(
        ProviderOffering, ProviderOffering.provider_offering_id == Booking.provider_offering_id
    ).join(
        Offering, Offering.offering_id == ProviderOffering.offering_id
    ).join(
        ServiceLocation, ServiceLocation.location_id == ProviderOffering.location_id
    ).filter(
        ProviderOffering.provider_id == provider_id
    )

    bookings = [{
        "booking_id": row.booking_id,
        "status": row.status,
        "appointment_date": str(row.appointment_date),
        "start_time": str(row.appointment_start_time),
        "end_time": str(row.appointment_end_time),
        "notes": row.notes,
        "user": {
            "name": row.user_name,
            "email": row.user_email
        },
        "service": row.service_name,
        "location": row.location_name
    } for row in query]

    return jsonify(bookings)


@provider_ai_bp.route("/ai/provider/respond", methods=["POST"])
def provider_respond_booking():
    """
    Respond to a Booking Request
    ---
    tags:
      - Provider AI Agent
    parameters:
      - in: body
        name: response
        required: true
        schema:
          type: object
          required: [provider_id, booking_id, status]
          properties:
            provider_id:
              type: string
              description: UUID of the provider
            booking_id:
              type: string
              description: UUID of the booking
            status:
              type: string
              description: New status (Confirmed, Cancelled, Rescheduled)
            message:
              type: string
              description: Message to send to the user
    responses:
      200:
        description: Booking updated and message sent
        schema:
          type: object
          properties:
            message:
              type: string
    """
    data = request.get_json()

    booking = Booking.query.filter_by(booking_id=data["booking_id"]).first()
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    # Update status and timestamp
    booking.status = data.get("status", booking.status)
    booking.updated_at = datetime.utcnow()
    db.session.commit()

    # Log the provider's message
    conversation = Conversation(
        message_id=str(uuid.uuid4()),
        booking_id=booking.booking_id,
        user_id=booking.user_id,
        provider_id=data["provider_id"],
        message_text=data.get("message", ""),
        sent_at=datetime.utcnow()
    )
    db.session.add(conversation)
    db.session.commit()

    return jsonify({"message": "Response recorded"})



@provider_ai_bp.route("/ai/provider/<provider_id>/conversations", methods=["GET"])
def provider_conversations(provider_id):
    """
    Get All Conversations for a Provider
    ---
    tags:
      - Provider AI Agent
    parameters:
      - name: provider_id
        in: path
        required: true
        type: string
        description: UUID of the provider
    responses:
      200:
        description: List of conversation messages
        schema:
          type: array
          items:
            type: object
            properties:
              message_id:
                type: string
              booking_id:
                type: string
              user_id:
                type: string
              message_text:
                type: string
              sent_at:
                type: string
    """
    conversations = Conversation.query.filter_by(provider_id=provider_id).order_by(Conversation.sent_at.desc()).all()

    return jsonify([{
        "message_id": c.message_id,
        "booking_id": c.booking_id,
        "user_id": c.user_id,
        "message_text": c.message_text,
        "sent_at": c.sent_at.isoformat()
    } for c in conversations])
