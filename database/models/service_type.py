from db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class ServiceType(db.Model):
    __tablename__ = 'service_types'

    type_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type_name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('service_categories.category_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "type_id": str(self.type_id),
            "type_name": self.type_name,
            "category_id": str(self.category_id),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
