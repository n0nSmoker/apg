from app.users.models import User


def get_user_by_id(user_id: int) -> User:
    return User.query.get(user_id)
