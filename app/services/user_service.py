from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def create_user(self, user_body, db):
        return self.repository.create_user(user_body, db)

    def auth_user(self, user_body, db):
        return self.repository.auth_user(user_body, db)

    def check_if_user_exists(self, login, db):
        return True if len(self.repository.get_user(login, db)) == 1 else False

    def get_user_by_id(self, user_id, db):
        return self.repository.get_user_by_id(user_id, db)

    def get_user_by_nickname(self, nickname, db):
        return self.repository.get_user_by_nick(nickname, db)
