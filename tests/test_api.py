full_payload = {
    "name": "First dashboard",
    "cockpit": [
        "balance_value-cum-y",
        "sell_value-cum-y",
        "sell_value-cum-m",
        "buy_value-cum-m",
    ],
    "sections": [
        {
            "name": "section_A",
            "graph": "buy_value",
            "graphKPIs": ["buy_price-avg-m", "buy_price-lstdff-m"],
        },
        {
            "name": "section_B",
            "graph": "balance_value",
            "graphKPIs": ["balance_value-cum-y", "balance_value-lstdff-m"],
        },
    ],
}


def test_create_dashboard(client):
    result = client.post("/dashboard", json=full_payload)
    assert result.status_code == 201


def test_get_dashboard(client, dashboard_id):
    result = client.get(f"/dashboard/{dashboard_id}")
    assert result.status_code == 200
    assert result.json == {"name": "Sample dashboard", "cockpit": [], "sections": []}

    id = "0e36a56c-e22b-43df-96c1-a2caccc29a5d"
    result = client.get(f"/dashboard/{id}")
    assert result.status_code == 404
    assert result.json == {"message": f"dashboard {id} not found"}


def test_get_dashboard_data(client, dashboard_id, dashboard_layout):
    result = client.get(f"/dashboard/{dashboard_id}/data")

    assert result.status_code == 200
