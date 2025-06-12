from db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class ServiceLocation(db.Model):
    __tablename__ = 'service_locations'

    location_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.Text)
    latitude = db.Column(db.Numeric)
    longitude = db.Column(db.Numeric)
    type_id = db.Column(UUID(as_uuid=True), db.ForeignKey('service_types.type_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "location_id": str(self.location_id),
            "name": self.name,
            "address": self.address,
            "latitude": str(self.latitude) if self.latitude else None,
            "longitude": str(self.longitude) if self.longitude else None,
            "type_id": str(self.type_id),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
