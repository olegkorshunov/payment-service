import logging.config
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
from redis.asyncio import Redis
from starlette.exceptions import HTTPException

from app import api, config

logging.config.dictConfig(config.LOGGING)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = Redis(host=config.redis.host, port=config.redis.port, password=config.redis.password)
    yield
    # Note: redis stubs incorrect
    await app.state.redis.aclose()  # type: ignore


app = FastAPI(
    title=config.application.name,
    version=config.application.version,
    debug=config.application.debug,
    docs_url=config.application.docs_url,
    root_path=config.application.root_path,
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

instrumentator = Instrumentator().instrument(app)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)


app.include_router(api.v1.router, prefix="/api/v1")
