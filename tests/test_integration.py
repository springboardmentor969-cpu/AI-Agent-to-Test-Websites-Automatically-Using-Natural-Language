import requests

def test_submit_test_api():
    url = "http://127.0.0.1:5000/api/submit_test"
    payload = "test login flow"

    response = requests.post(url, data=payload)

    assert response.status_code == 200

    data = response.json()

    # Updated checks for current Milestone-3 output structure
    assert "action_plan" in data
    assert "generated_code" in data
    assert "report" in data
    assert "instruction" in data

    # action plan must contain steps
    assert isinstance(data["action_plan"]["steps"], list)
    assert len(data["action_plan"]["steps"]) > 0

    # report must contain at least 1 command
    assert len(data["report"]) >= 1