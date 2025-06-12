from flask import Blueprint, request, jsonify

from database.models.service_category import ServiceCategory
from database.models.offering import Offering
from database.models.provider import Provider
from database.models.service_location import ServiceLocation
from database.models.service_type import ServiceType

from db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from geopy.distance import geodesic