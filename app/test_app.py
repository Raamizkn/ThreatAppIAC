import json
import pytest
from app import app, ThreatDetector

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    """Test the health endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'status' in data
    assert data['status'] == 'healthy'
    assert 'timestamp' in data

def test_detect_endpoint_safe_text(client):
    """Test the detect endpoint with safe text"""
    response = client.post('/api/detect', 
                          json={'text': 'Hello, can we schedule a meeting tomorrow?'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'is_threat' in data
    assert data['is_threat'] is False
    assert 'confidence' in data
    assert 'timestamp' in data

def test_detect_endpoint_threat_text(client):
    """Test the detect endpoint with threat text"""
    response = client.post('/api/detect', 
                          json={'text': 'URGENT: Your account has been compromised, click here to reset your password'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'is_threat' in data
    assert data['is_threat'] is True
    assert 'confidence' in data
    assert 'timestamp' in data

def test_detect_endpoint_invalid_request(client):
    """Test the detect endpoint with invalid request"""
    response = client.post('/api/detect', json={})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_batch_detect_endpoint(client):
    """Test the batch detect endpoint"""
    texts = [
        "Hello, can we schedule a meeting tomorrow?",
        "URGENT: Your account has been compromised, click here to reset your password"
    ]
    response = client.post('/api/batch-detect', json={'texts': texts})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'results' in data
    assert len(data['results']) == 2
    assert data['results'][0]['is_threat'] is False
    assert data['results'][1]['is_threat'] is True

def test_threat_detector_class():
    """Test the ThreatDetector class"""
    detector = ThreatDetector()
    
    # Test safe text
    result = detector.predict("Hello, how are you doing today?")
    assert result['is_threat'] is False
    assert 'confidence' in result
    assert 'timestamp' in result
    
    # Test threat text
    result = detector.predict("URGENT: Your account has been compromised")
    assert result['is_threat'] is True
    assert 'confidence' in result
    assert 'timestamp' in result 