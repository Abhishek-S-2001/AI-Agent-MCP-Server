from imports import *
from db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class ServiceCategory(db.Model):
    __tablename__ = 'service_categories'

    category_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_name = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "category_id": str(self.category_id),
            "category_name": self.category_name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
