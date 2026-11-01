# tests/test_health.py
# Signature: Mourad.Soltani

import pytest
from app import app, check_url

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'
    assert data['service'] == 'URLPulse'
    assert data['signature'] == 'Mourad.Soltani'

def test_check_url_healthy():
    # Use a known good URL
    result = check_url('https://httpbin.org/status/200')
    assert result['healthy'] is True
    assert result['status_code'] == 200
    assert result['error'] is None
    assert result['response_time_ms'] >= 0

def test_check_url_unhealthy():
    result = check_url('https://httpbin.org/status/500')
    assert result['healthy'] is False
    assert result['status_code'] == 500

def test_api_check_no_urls(client):
    response = client.post('/api/check', json={'urls': []})
    assert response.status_code == 400

def test_api_check_valid(client):
    response = client.post('/api/check', json={'urls': ['https://httpbin.org/status/200']})
    assert response.status_code == 200
    data = response.get_json()
    assert 'results' in data
    assert data['summary']['total'] == 1
    assert data['summary']['healthy'] == 1
