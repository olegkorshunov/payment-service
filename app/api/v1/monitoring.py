from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from sqlalchemy import select

from app.db.registry import ASYNC_SESSION_MAKER

router = APIRouter()


@router.get(
    "/ping",
    responses={"200": {"content": {"application/json": {"example": {"status": "OK"}}}}},
    response_class=ORJSONResponse,
)
async def ping() -> ORJSONResponse:
    """Health check for service"""
    async with ASYNC_SESSION_MAKER() as session:
        res = await session.execute(select(1))
    return ORJSONResponse({"status": "OK", "database": res.scalar_one_or_none()})
