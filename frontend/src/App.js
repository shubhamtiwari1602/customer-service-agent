import React, { useState } from 'react';
import './App.css';

// Environment-aware API URL configuration
const getApiUrl = () => {
  // Production API URL (replace with your deployed backend URL)
  if (process.env.NODE_ENV === 'production') {
    return process.env.REACT_APP_API_URL || 'https://your-api-domain.railway.app';
  }
  // Development API URL
  return 'http://localhost:8000';
};

const API_BASE_URL = getApiUrl();

const SentimentIcon = ({ sentiment }) => {
  const icons = {
    positive: '😊',
    negative: '😟',
    neutral: '😐'
  };
  return <span>{icons[sentiment] || '😐'}</span>;
};

const ClassificationBadge = ({ classification }) => {
  const classMap = {
    'Technical Support': 'technical-support',
    'Product Feature Request': 'feature-request',
    'Sales Lead': 'sales-lead'
  };
  
  return (
    <span className={`badge ${classMap[classification]}`}>
      {classification}
    </span>
  );
};

const ConfidenceBar = ({ confidence }) => {
  return (
    <div className="confidence-bar">
      <div 
        className="confidence-fill" 
        style={{ width: `${confidence * 100}%` }}
      ></div>
      <div className="confidence-text">
        Confidence: {Math.round(confidence * 100)}%
      </div>
    </div>
  );
};

const ProcessingIndicator = () => (
  <div className="processing-indicator">
    <span>Processing your request</span>
    <div className="dots">
      <div className="dot"></div>
      <div className="dot"></div>
      <div className="dot"></div>
    </div>
  </div>
);

function App() {
  const [query, setQuery] = useState('');
  const [companyName, setCompanyName] = useState('');
  const [teamSize, setTeamSize] = useState('');
  const [response, setResponse] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    
    setIsLoading(true);
    setError(null);
    setResponse(null);
    
    try {
      const res = await fetch(`${API_BASE_URL}/classify`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query.trim(),
          company_name: companyName.trim() || null,
          team_size: teamSize ? parseInt(teamSize) : null
        }),
      });
      
      if (!res.ok) {
        throw new Error(`Server error: ${res.status}`);
      }
      
      const data = await res.json();
      setResponse(data);
    } catch (error) {
      console.error('Error:', error);
      setError(error.message);
      setResponse({
        classification: 'Error',
        response: 'Failed to get response from server. Please check if the backend is running and try again.',
        needs_escalation: true,
        sentiment: 'neutral',
        confidence: 0
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setQuery('');
    setCompanyName('');
    setTeamSize('');
    setResponse(null);
    setError(null);
  };

  return (
    <div className="app">
      <div className="header">
        <h1>🤖 Customer Service Agent</h1>
        <p>Intelligent support powered by AI - Get instant help with your queries</p>
      </div>
      
      <div className="form-container">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="query">
              📝 What can we help you with today?
            </label>
            <textarea
              id="query"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Describe your question, issue, or request in detail..."
              required
              maxLength={2000}
            />
          </div>
          
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="companyName">
                🏢 Company Name (optional)
              </label>
              <input
                id="companyName"
                type="text"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
                placeholder="Your company name"
                maxLength={100}
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="teamSize">
                👥 Team Size (optional)
              </label>
              <input
                id="teamSize"
                type="number"
                value={teamSize}
                onChange={(e) => setTeamSize(e.target.value)}
                placeholder="Number of team members"
                min="1"
                max="10000"
              />
            </div>
          </div>
          
          <div style={{ display: 'flex', gap: '15px' }}>
            <button type="submit" className="submit-btn" disabled={isLoading || !query.trim()}>
              {isLoading && <span className="loading-spinner"></span>}
              {isLoading ? 'Processing...' : '🚀 Submit Query'}
            </button>
            
            {(query || companyName || teamSize || response) && (
              <button 
                type="button" 
                onClick={handleReset}
                className="submit-btn"
                style={{ 
                  background: '#e2e8f0', 
                  color: '#4a5568',
                  flex: '0 0 auto',
                  width: 'auto',
                  padding: '16px 24px'
                }}
              >
                🔄 Reset
              </button>
            )}
          </div>
        </form>
      </div>
      
      {isLoading && (
        <div className="response-container">
          <div className="response-card">
            <ProcessingIndicator />
          </div>
        </div>
      )}
      
      {response && !isLoading && (
        <div className="response-container">
          <div className={`response-card ${response.needs_escalation ? 'escalation' : ''}`}>
            <div className="response-header">
              <h2 className="response-title">
                {response.classification === 'Error' ? '❌ Error' : '✅ Response'}
              </h2>
              
              <div className="badge-container">
                {response.classification !== 'Error' && (
                  <ClassificationBadge classification={response.classification} />
                )}
                
                {response.sentiment && (
                  <div className={`sentiment-indicator ${response.sentiment}`}>
                    <SentimentIcon sentiment={response.sentiment} />
                    <span>{response.sentiment}</span>
                  </div>
                )}
              </div>
            </div>
            
            {response.confidence !== undefined && response.classification !== 'Error' && (
              <ConfidenceBar confidence={response.confidence} />
            )}
            
            <div className="response-content">
              {response.response}
            </div>
            
            {response.needs_escalation && (
              <div className="escalation-notice">
                <span className="icon">🚨</span>
                This request has been escalated to our priority support team for immediate attention.
              </div>
            )}
            
            <div className="status-indicators">
              <div style={{ fontSize: '0.85rem', color: '#718096' }}>
                Response generated in real-time
              </div>
              <div style={{ fontSize: '0.85rem', color: '#718096' }}>
                {new Date().toLocaleTimeString()}
              </div>
            </div>
          </div>
        </div>
      )}
      
      {error && (
        <div className="response-container">
          <div className="response-card escalation">
            <div className="response-header">
              <h2 className="response-title">⚠️ Connection Error</h2>
            </div>
            <div className="response-content">
              Unable to connect to the service. Please ensure the backend server is running on port 8000.
              <br /><br />
              <strong>Error details:</strong> {error}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
