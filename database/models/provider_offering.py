from db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class ProviderOffering(db.Model):
    __tablename__ = 'provider_offerings'

    provider_offering_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider_id = db.Column(UUID(as_uuid=True), db.ForeignKey("providers.provider_id"), nullable=False)
    offering_id = db.Column(UUID(as_uuid=True), db.ForeignKey("offerings.offering_id"), nullable=False)
    location_id = db.Column(UUID(as_uuid=True), db.ForeignKey("service_locations.location_id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "provider_offering_id": str(self.provider_offering_id),
            "provider_id": str(self.provider_id),
            "offering_id": str(self.offering_id),
            "location_id": str(self.location_id),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
