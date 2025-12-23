import requests

def test_submit_test_api():
    url = "http://127.0.0.1:5000/api/submit_test"
    payload = "test login flow"

    response = requests.post(url, data=payload)

    assert response.status_code == 200

    data = response.json()
    assert "job_id" in data
    assert data["status"] == "created"
    assert "action_plan" in data
