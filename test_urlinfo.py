from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_blocked_url_pulse():
    response = client.get(
        "/urlinfo/1/pulse.aws/%2Fapplication%2FW7SDDK2X%3Fp%3D0"
    )
    assert response.status_code == 200
    assert response.json()["verdict"] == "DENY"

def test_blocked_url_malware():
    response = client.get(
        "/urlinfo/1/malware.test/%2Fbad%2Fpath"
    )
    assert response.json()["verdict"] == "DENY"

def test_allowed_example():
    response = client.get(
        "/urlinfo/1/example.com/%2Fhome"
    )
    assert response.json()["verdict"] == "ALLOW"

def test_allowed_wikipedia():
    response = client.get(
        "/urlinfo/1/es.wikipedia.org/%2Fwiki%2FWikipedia%3APortada"
    )
    assert response.json()["verdict"] == "ALLOW"

def test_unknown_url():
    response = client.get(
        "/urlinfo/1/google.com/%2Fsearch"
    )
    assert response.json()["verdict"] == "UNKNOWN"
