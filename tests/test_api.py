from requests import post, get
from json import dumps
from pprint import pprint


full_payload = {
    
    "cockpit": ["balance-cum-y", "sell_value-cum-y", "sell_value-cum-m","buy_value-cum-m"],
    "dashboard_name": "First dashboard",
    "sectionList": [
        {"section_A" :{
            "graph": "buy_value",
            "graphKPIs" : ["cumulated_yearly", "cumulated_daily"]
            }},
        {"section_B" :{
            "graph": "sell_value",
            "graphKPIs" : ["cumulated_yearly", "cumulated_daily"]
            }}
        ]
}



def test_create_dashboard():
   
    result = post(url = "http://localhost:5000/create_dashboard",  json=full_payload)
    assert result.status_code == 201


def test_get_dashboard():
   
    payload = {
        "dashboard_name": "First dashboard"
    }
    result = get(url = "http://localhost:5000/get_dashboard",  params=payload)
    assert result.json()==full_payload
    assert 200


    result = get(url = "http://localhost:5000/get_dashboard",  params={"dashboard_name": "not exist"})
    assert result.status_code == 404
    assert result.json() == {"message":"not found"}

def test_get_dashboard_data():
   
    payload = {
        "dashboard_name": "First dashboard"
    }
    result = get(url = "http://localhost:5000/get_dashboard_data",  params=payload)
    pprint(result)
