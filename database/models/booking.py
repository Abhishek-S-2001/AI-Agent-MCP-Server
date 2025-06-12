from db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class Booking(db.Model):
    __tablename__ = 'bookings'

    booking_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider_offering_id = db.Column(UUID(as_uuid=True), db.ForeignKey("provider_offerings.provider_offering_id"), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.user_id"), nullable=False)
    booking_time = db.Column(db.DateTime)
    appointment_date = db.Column(db.Date)
    appointment_start_time = db.Column(db.Time)
    appointment_end_time = db.Column(db.Time)
    status = db.Column(db.String(20), default='pending')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "booking_id": str(self.booking_id),
            "provider_offering_id": str(self.provider_offering_id),
            "user_id": str(self.user_id),
            "booking_time": self.booking_time.isoformat() if self.booking_time else None,
            "appointment_date": self.appointment_date.isoformat() if self.appointment_date else None,
            "appointment_start_time": str(self.appointment_start_time) if self.appointment_start_time else None,
            "appointment_end_time": str(self.appointment_end_time) if self.appointment_end_time else None,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
