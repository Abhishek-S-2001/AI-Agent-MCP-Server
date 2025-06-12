from db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class Conversation(db.Model):
    __tablename__ = 'conversations'

    message_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    booking_id = db.Column(UUID(as_uuid=True), db.ForeignKey("bookings.booking_id"), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.user_id"), nullable=False)
    provider_id = db.Column(UUID(as_uuid=True), db.ForeignKey("providers.provider_id"), nullable=False)
    message_text = db.Column(db.Text)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "message_id": str(self.message_id),
            "booking_id": str(self.booking_id),
            "user_id": str(self.user_id),
            "provider_id": str(self.provider_id),
            "message_text": self.message_text,
            "sent_at": self.sent_at.isoformat()
        }
