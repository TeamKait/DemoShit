from app.db.service import DBService


class AuthService:
    def __init__(self, db_service: DBService):
        self.db = db_service

    async def login(self, login: str, password: str):
        user = await self.db.get_user_by_login(login)
        if user is None:
            return False
        return user.password == password
