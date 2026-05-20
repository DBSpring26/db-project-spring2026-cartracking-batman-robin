from fastapi import APIRouter, Depends
from db.db import get_connection
from handlers.auth_handler import AuthHandler
from schemas.auth_schema import AuthRequest


auth_router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


def get_handler():
    conn = get_connection()
    try:
        yield AuthHandler(conn)
    finally:
        conn.close()


@auth_router.post("/signup", status_code=201)
def signup(payload: AuthRequest, handler: AuthHandler = Depends(get_handler)):
    return handler.signup(payload.model_dump())


@auth_router.post("/login")
def login(payload: AuthRequest, handler: AuthHandler = Depends(get_handler)):
    return handler.login(payload.model_dump())