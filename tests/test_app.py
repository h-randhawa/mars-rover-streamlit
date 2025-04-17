import pytest
import requests

@pytest.fixture
def mock_manifest_response():
    return {
        "photo_manifest": {
            "name": "Curiosity",
            "landing_date": "2012-08-06",
            "launch_date": "2011-11-26",
            "status": "active",
            "max_sol": 4000,
            "max_date": "2024-04-16",
            "total_photos": 654321,
            "photos": []
        }
    }

def test_mock_manifest_request(requests_mock, mock_manifest_response):
    url = "https://api.nasa.gov/mars-photos/api/v1/manifests/curiosity"
    requests_mock.get(url, json=mock_manifest_response)

    res = requests.get(url)
    data = res.json()

    assert res.status_code == 200
    assert "photo_manifest" in data
    assert data["photo_manifest"]["name"] == "Curiosity"
    assert int(data["photo_manifest"]["total_photos"]) > 0
