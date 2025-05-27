import pytest
from fastapi.testclient import TestClient
from main import app
import json
import os
from pathlib import Path

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint returns correct information"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Customer Service Agent API"
    assert "version" in data

class TestTechnicalSupport:
    """Test technical support classification and responses"""
    
    def test_login_issue_classification(self):
        response = client.post(
            "/classify",
            json={"query": "I can't login to my account", "company_name": None, "team_size": None}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["classification"] == "Technical Support"
        assert "password" in data["response"].lower() or "login" in data["response"].lower()
        assert "sentiment" in data
        
    def test_payment_issue_classification(self):
        response = client.post(
            "/classify",
            json={"query": "My payment is not working", "company_name": None, "team_size": None}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["classification"] == "Technical Support"
        assert not data["needs_escalation"]  # Should find solution in KB
        
    def test_unknown_technical_issue(self):
        response = client.post(
            "/classify",
            json={"query": "Mysterious widget malfunction with symptoms ABC123", "company_name": None, "team_size": None}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["classification"] == "Technical Support"
        assert data["needs_escalation"]  # Should escalate unknown issues
        
    def test_negative_sentiment_escalation(self):
        response = client.post(
            "/classify",
            json={"query": "I'm extremely frustrated with this terrible login problem", "company_name": None, "team_size": None}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["classification"] == "Technical Support"
        assert data["sentiment"] == "negative"
        assert data["needs_escalation"]  # Negative sentiment should escalate

class TestFeatureRequests:
    """Test feature request classification and logging"""
    
    def test_feature_request_classification(self):
        response = client.post(
            "/classify",
            json={"query": "Please add dark mode feature", "company_name": None, "team_size": None}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["classification"] == "Product Feature Request"
        assert "thank" in data["response"].lower()
        assert not data["needs_escalation"]
        
    def test_feature_request_logging(self):
        test_request = "Add export to Excel functionality"
        response = client.post(
            "/classify",
            json={"query": test_request, "company_name": None, "team_size": None}
        )
        assert response.status_code == 200
        
        # Check if request was logged
        log_file = Path("feature_requests.log")
        assert log_file.exists()
        with open(log_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert test_request in content
            
    def test_improvement_suggestion(self):
        response = client.post(
            "/classify",
            json={"query": "Could you improve the UI to be more user-friendly?", "company_name": None, "team_size": None}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["classification"] == "Product Feature Request"

class TestSalesLeads:
    """Test sales lead classification and qualification"""
    
    def test_complete_sales_inquiry(self):
        response = client.post(
            "/classify",
            json={"query": "Interested in enterprise pricing", "company_name": "TechCorp", "team_size": 50}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["classification"] == "Sales Lead"
        assert "TechCorp" in data["response"]
        assert not data["needs_escalation"]
        
    def test_missing_company_info(self):
        response = client.post(
            "/classify",
            json={"query": "What are your prices?", "company_name": None, "team_size": 25}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["classification"] == "Sales Lead"
        assert data["needs_escalation"]
        assert "company name" in data["response"].lower()
        
    def test_missing_team_size(self):
        response = client.post(
            "/classify",
            json={"query": "Pricing information needed", "company_name": "StartupCo", "team_size": None}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["classification"] == "Sales Lead"
        assert data["needs_escalation"]
        assert "team size" in data["response"].lower()
        
    def test_large_enterprise_escalation(self):
        response = client.post(
            "/classify",
            json={"query": "Enterprise solution needed", "company_name": "BigCorp", "team_size": 500}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["classification"] == "Sales Lead"
        assert data["needs_escalation"]  # Large teams should escalate
        assert "Enterprise" in data["response"]

class TestSentimentAnalysis:
    """Test sentiment analysis functionality"""
    
    def test_positive_sentiment(self):
        response = client.post(
            "/classify",
            json={"query": "I love your product! Just need help with login", "company_name": None, "team_size": None}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["sentiment"] in ["positive", "neutral"]
        
    def test_negative_sentiment(self):
        response = client.post(
            "/classify",
            json={"query": "This is awful, nothing works properly", "company_name": None, "team_size": None}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["sentiment"] == "negative"
        assert data["needs_escalation"]  # Negative sentiment should escalate

class TestInputValidation:
    """Test input validation and error handling"""
    
    def test_missing_query(self):
        response = client.post(
            "/classify",
            json={"company_name": "TestCo", "team_size": 10}
        )
        assert response.status_code == 422  # Validation error
        
    def test_empty_query(self):
        response = client.post(
            "/classify",
            json={"query": "", "company_name": None, "team_size": None}
        )
        assert response.status_code == 422  # Validation error
        
    def test_invalid_team_size(self):
        response = client.post(
            "/classify",
            json={"query": "sales inquiry", "company_name": "TestCo", "team_size": -5}
        )
        assert response.status_code == 200  # Should handle gracefully
        
    def test_very_long_query(self):
        long_query = "help " * 1000  # Very long query
        response = client.post(
            "/classify",
            json={"query": long_query, "company_name": None, "team_size": None}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["classification"] == "Technical Support"

class TestConfidenceScoring:
    """Test confidence scoring for classifications"""
    
    def test_high_confidence_technical(self):
        response = client.post(
            "/classify",
            json={"query": "login error problem help issue", "company_name": None, "team_size": None}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["classification"] == "Technical Support"
        assert data["confidence"] > 0.5
        
    def test_low_confidence_ambiguous(self):
        response = client.post(
            "/classify",
            json={"query": "hello", "company_name": None, "team_size": None}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["confidence"] >= 0.0

def test_cleanup():
    """Clean up test files"""
    log_file = Path("feature_requests.log")
    if log_file.exists():
        # Keep the log file but we could clean it up if needed
        pass
