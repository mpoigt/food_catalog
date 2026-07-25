from decimal import Decimal


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


async def _create_category(client, token: str, name: str) -> str:
    r = await client.post("/categories/", headers=_auth(token), json={"name": name})
    assert r.status_code == 201
    return r.json()["id"]


async def _create_product(client, token: str, category_id: str, **overrides) -> dict:
    body = {
        "name": "Селедка",
        "category_id": category_id,
        "description": "Селедка соленая",
        "price": "10.00",
        "note_common": "Акция",
        "note_special": "Пересоленая",
    }
    body.update(overrides)
    r = await client.post("/products/", headers=_auth(token), json=body)
    return r


async def test_advanced_manages_category(client, make_token):
    advanced = await make_token("ADVANCED", "adv@example.com")
    cid = await _create_category(client, advanced, "Еда")

    upd = await client.patch(
        f"/categories/{cid}", headers=_auth(advanced), json={"name": "Напитки"}
    )
    assert upd.status_code == 200
    assert upd.json()["name"] == "Напитки"

    listed = await client.get("/categories/", headers=_auth(advanced))
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    deleted = await client.delete(f"/categories/{cid}", headers=_auth(advanced))
    assert deleted.status_code == 204


async def test_simple_user_cannot_manage_category(client, make_token):
    admin = await make_token("ADMIN", "admin2@example.com")
    simple = await make_token("USER", "user@example.com")
    cid = await _create_category(client, admin, "Еда")

    created = await client.post(
        "/categories/", headers=_auth(simple), json={"name": "Вода"}
    )
    assert created.status_code == 403

    updated = await client.patch(
        f"/categories/{cid}", headers=_auth(simple), json={"name": "X"}
    )
    assert updated.status_code == 403

    deleted = await client.delete(f"/categories/{cid}", headers=_auth(simple))
    assert deleted.status_code == 403


async def test_simple_user_can_add_and_edit_product_but_not_delete(client, make_token):
    advanced = await make_token("ADVANCED", "adv@example.com")
    simple = await make_token("USER", "user@example.com")
    cid = await _create_category(client, advanced, "Еда")

    created = await _create_product(client, simple, cid, name="Квас")
    assert created.status_code == 201
    pid = created.json()["id"]

    updated = await client.patch(
        f"/products/{pid}", headers=_auth(simple), json={"price": "12.50"}
    )
    assert updated.status_code == 200
    assert Decimal(str(updated.json()["price"])) == Decimal("12.50")

    deleted = await client.delete(f"/products/{pid}", headers=_auth(simple))
    assert deleted.status_code == 403


async def test_advanced_can_delete_product(client, make_token):
    advanced = await make_token("ADVANCED", "adv@example.com")
    cid = await _create_category(client, advanced, "Еда")
    pid = (await _create_product(client, advanced, cid)).json()["id"]

    deleted = await client.delete(f"/products/{pid}", headers=_auth(advanced))
    assert deleted.status_code == 204


async def test_note_special_hidden_for_simple_user(client, make_token):
    advanced = await make_token("ADVANCED", "adv@example.com")
    simple = await make_token("USER", "user@example.com")
    cid = await _create_category(client, advanced, "Еда")
    pid = (
        await _create_product(client, advanced, cid, note_special="Пересоленая")
    ).json()["id"]

    as_simple = await client.get(f"/products/{pid}", headers=_auth(simple))
    assert as_simple.status_code == 200
    assert as_simple.json()["note_special"] is None

    as_advanced = await client.get(f"/products/{pid}", headers=_auth(advanced))
    assert as_advanced.json()["note_special"] == "Пересоленая"


async def test_simple_user_cannot_set_note_special(client, make_token):
    advanced = await make_token("ADVANCED", "adv@example.com")
    simple = await make_token("USER", "user@example.com")
    cid = await _create_category(client, advanced, "Еда")

    created = await _create_product(
        client, simple, cid, name="Квас", note_special="Секрет"
    )
    assert created.status_code == 201
    pid = created.json()["id"]

    as_advanced = await client.get(f"/products/{pid}", headers=_auth(advanced))
    assert as_advanced.json()["note_special"] is None


async def test_usd_rate_endpoint(client, make_token):
    user = await make_token("USER", "user@example.com")

    r = await client.get("/currency/usd-rate", headers=_auth(user))
    assert r.status_code == 200
    body = r.json()
    assert Decimal(str(body["rate"])) == Decimal("3.00")
    assert body["date"] == "2026-07-22"


async def test_cascade_delete_removes_products(client, make_token):
    advanced = await make_token("ADVANCED", "adv@example.com")
    cid = await _create_category(client, advanced, "Еда")
    await _create_product(client, advanced, cid, name="Селедка")
    await _create_product(client, advanced, cid, name="Тушенка")

    deleted = await client.delete(f"/categories/{cid}", headers=_auth(advanced))
    assert deleted.status_code == 204

    listed = await client.get(
        "/products/", headers=_auth(advanced), params={"category_id": cid}
    )
    assert listed.json()["total"] == 0


async def test_search_and_filter(client, make_token):
    advanced = await make_token("ADVANCED", "adv@example.com")
    food = await _create_category(client, advanced, "Еда")
    water = await _create_category(client, advanced, "Вода")
    await _create_product(client, advanced, food, name="Селедка", description="Селедка соленая")
    await _create_product(client, advanced, food, name="Тушенка", description="Тушенка говяжья")
    await _create_product(client, advanced, water, name="Квас", description="В бутылках")

    found = await client.get(
        "/products/", headers=_auth(advanced), params={"search": "Тушен"}
    )
    assert found.json()["total"] == 1

    in_food = await client.get(
        "/products/", headers=_auth(advanced), params={"category_id": food}
    )
    assert in_food.json()["total"] == 2


async def test_price_usd_endpoint(client, make_token):
    advanced = await make_token("ADVANCED", "adv@example.com")
    cid = await _create_category(client, advanced, "Вкусности")
    pid = (
        await _create_product(client, advanced, cid, name="Сгущенка", price="30.00")
    ).json()["id"]

    r = await client.get(f"/products/{pid}/price-usd", headers=_auth(advanced))
    assert r.status_code == 200
    body = r.json()
    assert Decimal(str(body["price_byn"])) == Decimal("30.00")
    assert Decimal(str(body["price_usd"])) == Decimal("10.00")


async def test_catalog_requires_auth(client):
    assert (await client.get("/categories/")).status_code in (401, 403)
    assert (await client.get("/products/")).status_code in (401, 403)
