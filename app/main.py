from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from loguru import logger
from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from app.api.v1.api import api_router
from app.core.config import settings
from app.middlewares import ProcessTimeHeaderMiddleware

from .db import get_db, init_db
from .logger import setup_logging
from .models import Member


@asynccontextmanager
async def startup_event(app: FastAPI):
    """
    초기 실행 시, DB 정상 접속 여부를 확인
    """
    db: AsyncSession | None = None
    try:
        db = await anext(get_db())

        await init_db()
        if settings.ENV == "development":
            is_member = (await db.exec(select(func.count()).select_from(Member))).first()

            if not is_member:
                db.add(
                    Member(
                        email="admin@mail.com",
                        name="홍길동",
                        phone="+821046082710",
                    )
                )
                await db.commit()
    except Exception as e:
        logger.error(e)
    finally:
        if db:
            await db.close()
    yield
    logger.info("Shutdown")


# FastAPI
if settings.ENV == "development":
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"/{settings.API_V1_STR}/openapi.json",
        redoc_url=None,
        docs_url="/api/v1/docs",
        lifespan=startup_event,
    )

    @app.get("/", include_in_schema=False)
    async def docs_redirect() -> RedirectResponse:
        return RedirectResponse(url="/api/v1/docs")

else:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"/{settings.API_V1_STR}/openapi.json",
        redoc_url=None,
        docs_url=None,
    )
# Routes
app.include_router(api_router)

# Logger
setup_logging()

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.add_middleware(ProcessTimeHeaderMiddleware)


@app.exception_handler(500)
async def handle_500_errors(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"Error: {exc}, {request}")
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
