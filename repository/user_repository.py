users_db = []


def save_user(user):
    users_db.append(user)


def find_by_email(email):
    for user in users_db:
        if user.email == email:
            return user
    return None


def get_all_users():
    return users_db