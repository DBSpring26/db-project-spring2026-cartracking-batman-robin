from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/vehicles",
    tags=["vehicles"]
)

@router.get("/test")
def test_route():
    return {"message": "vehicle routes working"}