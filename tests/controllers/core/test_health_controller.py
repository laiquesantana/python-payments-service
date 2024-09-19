from httpx import AsyncClient

from app.main import app


async def test_health_index():
    """Test if the health index is accessible."""
    async with AsyncClient(app=app, base_url="http://t") as ac:
        response = await ac.get("/core/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "app": "Fastapi Base",
        "version": "1.0.0",
        "env": "test",
        "root_path": "",
    }
