from db import db
from datetime import datetime

class Booking(db.Model):
    __tablename__ = 'bookings'

    booking_id = db.Column(db.Integer, primary_key=True)
    service_offering_id = db.Column(db.Integer, nullable=False)
    booking_time = db.Column(db.DateTime, default=datetime.utcnow)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_start_time = db.Column(db.Time, nullable=False)
    appointment_end_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(50), default='pending')
    notes = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.String, nullable=False)
    provider_id = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "booking_id": self.booking_id,
            "service_offering_id": self.service_offering_id,
            "booking_time": self.booking_time.isoformat(),
            "appointment_date": self.appointment_date.isoformat(),
            "appointment_start_time": str(self.appointment_start_time),
            "appointment_end_time": str(self.appointment_end_time),
            "status": self.status,
            "notes": self.notes,
            "user_id": self.user_id,
            "provider_id": self.provider_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
