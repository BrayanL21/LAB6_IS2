from repository.user_repository import save_user, find_by_email
from models.user import User


def register_user(email, password, role):
    existing = find_by_email(email)

    if existing:
        return {"error": "User already exists"}

    user = User(email, password, role)
    save_user(user)

    return {"message": "User registered successfully"}


def login_user(email, password):
    user = find_by_email(email)

    if not user:
        return {"error": "User not found"}

    if user.password != password:
        return {"error": "Invalid credentials"}

    return {"message": "Login successful", "role": user.role}