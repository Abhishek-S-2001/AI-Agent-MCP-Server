from db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class Provider(db.Model):
    __tablename__ = 'providers'

    provider_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name = db.Column(db.String(150))
    license_number = db.Column(db.String(100))
    email = db.Column(db.String(100)) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "provider_id": str(self.provider_id),
            "company_name": self.company_name,
            "license_number": self.license_number,
            "email": self.email,  
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
