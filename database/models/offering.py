from db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class Offering(db.Model):
    __tablename__ = 'offerings'

    offering_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    offering_name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Numeric, nullable=True)
    availability_hours = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "offering_id": str(self.offering_id),
            "offering_name": self.offering_name,
            "price": float(self.price) if self.price else None,
            "availability_hours": self.availability_hours,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
