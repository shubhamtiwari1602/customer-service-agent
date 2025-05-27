# 🤖 Customer Service Agent

A sophisticated AI-powered customer service solution with a FastAPI backend and React frontend. The system intelligently classifies customer queries, provides automated responses, and escalates complex issues when needed.

## 🌟 Features

### Core Functionality
- **Intelligent Query Classification**: Automatically categorizes queries into Technical Support, Product Feature Requests, or Sales Leads
- **Sentiment Analysis**: Analyzes customer emotions and escalates negative sentiment cases
- **Knowledge Base Search**: Searches through a comprehensive knowledge base for technical solutions
- **Automatic Escalation**: Smart escalation for complex issues, negative sentiment, or missing information
- **Feature Request Logging**: Automatically logs feature requests for product team review
- **Sales Lead Qualification**: Collects necessary information for sales follow-up

### Technical Features
- **RESTful API**: Well-documented FastAPI backend with automatic OpenAPI documentation
- **Real-time Processing**: Instant response generation with confidence scoring
- **CORS Support**: Configured for cross-origin requests
- **Input Validation**: Comprehensive request validation with helpful error messages
- **Comprehensive Testing**: Full test suite covering all functionality paths

### UI/UX Features
- **Modern Interface**: Beautiful, responsive design with gradient backgrounds and animations
- **Real-time Feedback**: Loading states, processing indicators, and instant responses
- **Sentiment Visualization**: Visual indicators for detected sentiment (😊😟😐)
- **Confidence Scoring**: Progress bars showing classification confidence levels
- **Escalation Alerts**: Clear visual indicators when requests require human attention
- **Mobile Responsive**: Optimized for all device sizes

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (tested with Python 3.13)
- Node.js 14+ and npm
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd customer_service_agent
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd ../frontend
   npm install
   ```

### Running the Application

1. **Start the Backend** (in backend directory)
   ```bash
   source venv/bin/activate
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   Backend will be available at: http://localhost:8000

2. **Start the Frontend** (in frontend directory)
   ```bash
   npm start
   ```
   Frontend will be available at: http://localhost:3000

## 📚 API Documentation

### Endpoints

#### `GET /`
Returns API information and version.

#### `POST /classify`
Classifies customer queries and generates responses.

**Request Body:**
```json
{
  "query": "I can't login to my account",
  "company_name": "TechCorp",  // optional
  "team_size": 50              // optional
}
```

**Response:**
```json
{
  "classification": "Technical Support",
  "response": "I found the following solution(s):\n\nTry resetting your password...",
  "needs_escalation": false,
  "sentiment": "neutral",
  "confidence": 0.85
}
```

### Interactive Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 Testing

### Backend Tests
```bash
cd backend
source venv/bin/activate
pytest test_api.py -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Test Coverage
- ✅ Query classification accuracy
- ✅ Sentiment analysis functionality
- ✅ Knowledge base search
- ✅ Escalation logic
- ✅ Input validation
- ✅ API response formats
- ✅ Error handling

## 🏗️ Architecture

### Backend (FastAPI)
```
backend/
├── main.py              # Main API application
├── kb.md                # Knowledge base content
├── test_api.py          # Comprehensive test suite
├── requirements.txt     # Python dependencies
└── feature_requests.log # Logged feature requests
```

### Frontend (React)
```
frontend/
├── src/
│   ├── App.js          # Main React component
│   ├── App.css         # Styles with animations
│   └── index.js        # React entry point
├── public/
│   ├── index.html      # HTML template
│   └── manifest.json   # PWA manifest
└── package.json        # Node dependencies
```

## 🎯 Classification Logic

### Technical Support
**Triggers:** help, issue, problem, error, bug, login, password, performance, slow, api, integration
**Actions:**
- Searches knowledge base for solutions
- Provides step-by-step troubleshooting
- Escalates if no solution found or negative sentiment

### Product Feature Request
**Triggers:** feature, request, suggestion, improvement, add, enhancement, new
**Actions:**
- Logs request with timestamp to feature_requests.log
- Acknowledges request professionally
- Provides timeline expectations

### Sales Lead
**Triggers:** price, pricing, cost, buy, purchase, upgrade, enterprise, demo, sales
**Actions:**
- Collects company name and team size
- Recommends appropriate plan tier
- Escalates large enterprise leads (>100 users)

## 🔧 Configuration

### Environment Variables
- `BACKEND_URL`: Backend API URL (default: http://localhost:8000)
- `CORS_ORIGINS`: Allowed CORS origins for API

### Customization
- **Knowledge Base**: Edit `backend/kb.md` to update solutions
- **Classification Keywords**: Modify keyword lists in `main.py`
- **Styling**: Update CSS variables in `App.css`
- **Business Logic**: Adjust escalation rules in handler functions

## 📈 Advanced Features

### Sentiment Analysis
- Uses TextBlob for natural language sentiment detection
- Automatically escalates negative sentiment (polarity < -0.1)
- Provides confidence scores for sentiment classification

### Confidence Scoring
- Keyword-based confidence calculation
- Visual progress bars in UI
- Higher confidence for more keyword matches

### Escalation Logic
- Unknown technical issues → Escalate
- Negative sentiment → Escalate
- Missing sales information → Escalate
- Large enterprise deals (>100 users) → Escalate

## 🚀 Deployment

### Production Considerations
- Use Gunicorn for backend: `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker`
- Build React for production: `npm run build`
- Configure proper CORS origins
- Set up SSL/HTTPS
- Use environment variables for configuration
- Implement rate limiting
- Add authentication if needed

### Docker Deployment
```dockerfile
# Backend Dockerfile example
FROM python:3.11-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Check the API documentation at `/docs`
- Review the comprehensive test suite
- Open an issue for bugs or feature requests

## 📊 Example Interactions

### Technical Support Query
```
User: "I can't log into my account"
Response: Login solution with password reset steps
Escalation: Only if negative sentiment detected
```

### Feature Request
```
User: "Please add dark mode"
Response: Professional acknowledgment with timeline
Escalation: No (logged for product team)
```

### Sales Inquiry
```
User: "What's your enterprise pricing?"
Response: Request for company details and team size
Escalation: Yes (missing information required)
```

---

🎉 **Ready to provide exceptional customer service with AI!**
