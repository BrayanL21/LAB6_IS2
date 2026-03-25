from flask import Blueprint, request, jsonify
from services.auth_service import register_user, login_user
from repository.user_repository import get_all_users

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    if len(password) < 4:
        return jsonify({"error": "Password too short"}), 400

    if "@" not in email:
        return jsonify({"error": "Invalid email format"}), 400

    response = register_user(email, password, role)

    if "error" in response:
        return jsonify(response), 400

    return jsonify(response), 201


@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    response = login_user(email, password)

    if "error" in response:
        return jsonify(response), 401

    return jsonify(response), 200


@auth_blueprint.route("/users", methods=["GET"])
def list_users():
    users = get_all_users()
    result = []

    for user in users:
        result.append({
            "email": user.email,
            "role": user.role
        })

    return jsonify(result), 200