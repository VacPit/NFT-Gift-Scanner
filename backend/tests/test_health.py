async def test_health(client):
    r = await client.get("/api/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


async def test_health_db(client):
    r = await client.get("/api/health/db")
    assert r.status_code == 200


async def test_openapi_available(client):
    r = await client.get("/openapi.json")
    assert r.status_code == 200
    assert "/api/health" in r.json()["paths"]
