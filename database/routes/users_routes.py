from imports import *
from database.models.users import User
from datetime import datetime

user_bp = Blueprint("user", __name__)

@user_bp.route("/users", methods=["GET"])
def get_users():
    """
    Retrieve all users in the system.

    Returns:
        JSON list of all users.
    """
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@user_bp.route("/users/<uuid:user_id>", methods=["GET"])
def get_user(user_id):
    """
    Retrieve a specific user by user_id.

    Args:
        user_id (UUID): Unique identifier of the user.

    Returns:
        JSON object of the user if found, else 404.
    """
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())


@user_bp.route("/users", methods=["POST"])
def create_user():
    """
    Create a new user.

    Request JSON:
        - name (str): Full name of the user.
        - email (str): Unique email address.

    Returns:
        JSON of the created user and 201 status code.
    """
    data = request.get_json()
    if not data.get("name") or not data.get("email"):
        return jsonify({"error": "Both name and email are required."}), 400

    user = User(
        name=data["name"],
        email=data["email"],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@user_bp.route("/users/<uuid:user_id>", methods=["PUT"])
def update_user(user_id):
    """
    Update an existing user's name and/or email.

    Args:
        user_id (UUID): ID of the user to update.

    Request JSON:
        - name (optional): New name
        - email (optional): New email

    Returns:
        Updated user JSON.
    """
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    if "name" in data:
        user.name = data["name"]
    if "email" in data:
        user.email = data["email"]
    user.updated_at = datetime.utcnow()

    db.session.commit()
    return jsonify(user.to_dict())


@user_bp.route("/users/<uuid:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """
    Delete a user by user_id.

    Args:
        user_id (UUID): ID of the user to delete.

    Returns:
        Success message JSON.
    """
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully."})
