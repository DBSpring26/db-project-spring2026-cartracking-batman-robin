from fastapi import HTTPException
from dao.auth_dao import AuthDAO


class AuthHandler:
    def __init__(self, conn):
        self.dao = AuthDAO(conn)

    def signup(self, data):
        username = data["username"].strip()
        password = data["password"].strip()

        if not username or not password:
            raise HTTPException(status_code=400, detail="username and password are required")

        existing = self.dao.get_user_by_username(username)

        if existing:
            raise HTTPException(status_code=409, detail="username already exists")

        return self.dao.create_user(username, password)

    def login(self, data):
        username = data["username"].strip()
        password = data["password"].strip()

        user = self.dao.get_user_by_username(username)

        if not user or user["password"] != password:
            raise HTTPException(status_code=401, detail="invalid username or password")

        return {
            "message": "login successful",
            "user_id": user["user_id"],
            "username": user["username"]
        }