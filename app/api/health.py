from datetime import datetime, timezone

import psutil
from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.db.postgresql import get_db
from app.schemas import APIStatus

router = APIRouter()


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Api status",
            "model": APIStatus,
        },
    },
)
def health_api(db: AsyncSession = Depends(get_db)) -> APIStatus:
    """
    ### Get api health
    """

    process = psutil.Process()
    start_time = process.create_time()

    timestamp = datetime.now(timezone.utc).isoformat()
    uptime = str(datetime.now().timestamp() - start_time)

    return APIStatus(
        status="OK", timestamp=timestamp, version=settings.VERSION, uptime=uptime
    )
