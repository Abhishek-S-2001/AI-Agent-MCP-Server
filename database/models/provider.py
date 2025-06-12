from db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class Provider(db.Model):
    __tablename__ = 'providers'

    provider_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name = db.Column(db.String(150), nullable=False)
    license_number = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "provider_id": str(self.provider_id),
            "company_name": self.company_name,
            "license_number": self.license_number,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
