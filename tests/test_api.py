from requests import post, get, delete
from pytest import fixture


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


def test_create_dashboard(app_test):
    result = post(url="http://localhost:5000/dashboard", json=full_payload)
    assert result.status_code == 201


def test_get_dashboard():
    id = 1
    result = get(url=f"http://localhost:5000/dashboard/{id}")
    assert result.json() == full_payload
    assert 200

    id = 404
    result = get(url=f"http://localhost:5000/dashboard/{id}")
    assert result.status_code == 404
    assert result.json() == {"message": f"dashboard {id} not found"}


def test_get_dashboard_data():
    id = 1
    result = get(url=f"http://localhost:5000/dashboard/{id}/data")

    res_dict = result.json()

    assert result.status_code == 200
