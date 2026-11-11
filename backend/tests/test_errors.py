from fastapi import APIRouter
from pydantic import BaseModel

from app.core.errors import ConflictError, NotFoundError


class Payload(BaseModel):
    price: int


def _install(client):
    router = APIRouter()

    @router.get("/_t/notfound")
    async def nf():
        raise NotFoundError("Lot not found", details={"id": 1})

    @router.get("/_t/conflict")
    async def cf():
        raise ConflictError("Already exists")

    @router.get("/_t/boom")
    async def boom():
        raise RuntimeError("secret internals")

    @router.post("/_t/validate")
    async def validate(p: Payload):
        return p

    client._transport.app.include_router(router)


async def test_app_error_format(client):
    _install(client)
    r = await client.get("/_t/notfound")
    assert r.status_code == 404
    assert r.json() == {
        "error": {"code": "not_found", "message": "Lot not found", "details": {"id": 1}}
    }


async def test_conflict_code(client):
    _install(client)
    r = await client.get("/_t/conflict")
    assert r.status_code == 409 and r.json()["error"]["code"] == "conflict"


async def test_unknown_route_uses_unified_format(client):
    r = await client.get("/api/nope")
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "not_found"


async def test_validation_error_format(client):
    _install(client)
    r = await client.post("/_t/validate", json={"price": "abc"})
    assert r.status_code == 422
    body = r.json()["error"]
    assert body["code"] == "validation_error"
    assert body["details"][0]["field"] == "price"


async def test_unhandled_error_hides_internals():
    # Исключение без ASGI-обёртки httpx пробрасывается, поэтому проверяем через raise_app_exceptions=False.
    from httpx import ASGITransport, AsyncClient

    from app.main import create_app

    app = create_app()

    @app.get("/_t/boom")
    async def boom():
        raise RuntimeError("secret internals")

    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/_t/boom")
    assert r.status_code == 500
    assert "secret" not in r.text
    assert r.json()["error"]["code"] == "internal_error"
