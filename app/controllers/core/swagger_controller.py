from fastapi import APIRouter, Depends, openapi
from starlette.responses import JSONResponse

from app import main
from app.config.config import get_settings
from app.security.security import verify_basic_auth

router = APIRouter(
    tags=["core"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/openapi.json", include_in_schema=False)
async def get_open_api(username: str = Depends(verify_basic_auth)):
    """Get documentation of API from openapi.

    Args:
        username (str): Username after basic auth.

    """
    _ = username  # unused: used in verify_basic_auth
    app = main.app
    _routes = [
        route
        for route in app.routes
        if route.name not in ["get_open_api", "get_documentation"]  # type: ignore
    ]
    return JSONResponse(
        openapi.utils.get_openapi(
            title=app.title,
            version="1",
            routes=_routes,
            servers=[
                {
                    "url": get_settings().prefix_url_path,
                }
            ],
        )
    )


@router.get("/docs", include_in_schema=False)
async def get_documentation(username: str = Depends(verify_basic_auth)):
    """Get documentation of API from swagger ui.

    Args:
        username (str): Username after basic auth.

    """
    app = main.app
    _ = username  # unused: used in verify_basic_auth
    root_path = get_settings().prefix_url_path.rstrip("/")
    url = f"{root_path}/core/openapi.json"
    return openapi.docs.get_swagger_ui_html(
        openapi_url=url,
        title=f"{app.title} Documentation",
    )
