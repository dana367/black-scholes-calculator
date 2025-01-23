from api.endpoints import auth, black_scholes
from fastapi import APIRouter

api_router = APIRouter()


api_router.include_router(auth.router)
api_router.include_router(black_scholes.router)
