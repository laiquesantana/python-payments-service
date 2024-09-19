from fastapi import APIRouter

from app.config.config import get_settings

router = APIRouter(
    tags=["core"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/health")
async def health():
    """Health check endpoint."""

    settings = get_settings()
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.version,
        "env": settings.app_env,
        "root_path": settings.prefix_url_path,
    }
