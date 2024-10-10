from fastapi import APIRouter

from app.api.v1.wallet import router as wallet_router

from . import monitoring

router = APIRouter()
router.include_router(monitoring.router, tags=["monitoring"])
router.include_router(wallet_router, tags=["wallet"])
