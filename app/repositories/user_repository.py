from app.models import Users


class UserRepository:
    def get_users(self, db):
        return db.query(Users).all()

    def get_user_by_id(self, user_id, db):
        return db.query(Users).filter(Users.id == user_id).first()

    def get_user(self, login, db):
        return db.query(Users).filter(Users.login == login).all()

    def get_user_by_nick(self, nickname, db):
        return db.query(Users).filter(Users.nickname.ilike(f"{nickname}%")).all()

    def create_user(self, user_data: dict, db):
        user = Users(**user_data.dict())
        user.hashed_password = 'lolbek'
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


    def auth_user(self, user_data: dict, db):
        if len(db.query(Users).filter(Users.login == user_data.login and Users.password == user_data.password).all()) == 1:
            return db.query(Users).filter(Users.login == user_data.login and Users.password == user_data.password).first()
