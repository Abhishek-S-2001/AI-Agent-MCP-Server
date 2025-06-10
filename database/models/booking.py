from db import db
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

class Booking(db.Model):
    __tablename__ = 'bookings'

    booking_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_offering_id = db.Column(UUID(as_uuid=True), nullable=False)
    booking_time = db.Column(db.DateTime, default=datetime.utcnow)
    appointment_date = db.Column(db.Date, nullable=True)
    appointment_start_time = db.Column(db.Time, nullable=True)
    appointment_end_time = db.Column(db.Time, nullable=True)
    status = db.Column(db.String(20), default="pending")
    notes = db.Column(db.Text, nullable=True)
    user_id = db.Column(UUID(as_uuid=True), nullable=False)
    provider_id = db.Column(UUID(as_uuid=True), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "booking_id": str(self.booking_id),
            "service_offering_id": str(self.service_offering_id),
            "booking_time": self.booking_time.isoformat() if self.booking_time else None,
            "appointment_date": self.appointment_date.isoformat() if self.appointment_date else None,
            "appointment_start_time": str(self.appointment_start_time) if self.appointment_start_time else None,
            "appointment_end_time": str(self.appointment_end_time) if self.appointment_end_time else None,
            "status": self.status,
            "notes": self.notes,
            "user_id": str(self.user_id),
            "provider_id": str(self.provider_id),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
