from fastapi import APIRouter
from .routers.auth import router as auth_router


routers = APIRouter()


routers.include_router(auth_router)