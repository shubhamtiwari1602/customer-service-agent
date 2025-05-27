# 🚀 Local Setup Guide - Customer Service Agent

This guide will help you set up and run the Customer Service Agent system locally, including test cases to demonstrate all features.

## 📋 Prerequisites

Before starting, make sure you have:
- **Python 3.8+** (tested with Python 3.13)
- **Node.js 14+** and npm
- **Git** (for cloning)
- **Terminal/Command Line** access

### Check Your Versions
```bash
python3 --version    # Should be 3.8+
node --version       # Should be 14+
npm --version        # Should be 6+
```

## 🛠️ Step-by-Step Setup

### Step 1: Navigate to Project Directory
```bash
cd /Users/shubhamtiwari/Documents/nullai/customer_service_agent
```

### Step 2: Backend Setup (FastAPI)

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   ```

3. **Activate virtual environment**
   ```bash
   source venv/bin/activate
   ```
   > You should see `(venv)` in your terminal prompt

4. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Verify installation**
   ```bash
   pip list
   ```
   > Should show: fastapi, uvicorn, pydantic, textblob, pytest, httpx

### Step 3: Frontend Setup (React)

1. **Open a new terminal tab/window**
2. **Navigate to frontend directory**
   ```bash
   cd /Users/shubhamtiwari/Documents/nullai/customer_service_agent/frontend
   ```

3. **Install Node.js dependencies**
   ```bash
   npm install
   ```

4. **Verify installation**
   ```bash
   npm list --depth=0
   ```
   > Should show React, testing libraries, and other dependencies

## 🚀 Running the Application

### Terminal 1: Start Backend Server

1. **Navigate to backend and activate environment**
   ```bash
   cd /Users/shubhamtiwari/Documents/nullai/customer_service_agent/backend
   source venv/bin/activate
   ```

2. **Start FastAPI server**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Verify backend is running**
   - You should see: `Uvicorn running on http://0.0.0.0:8000`
   - Open browser: http://localhost:8000
   - Should show: `{"message":"Customer Service Agent API","version":"1.0.0"}`

### Terminal 2: Start Frontend Server

1. **Navigate to frontend directory**
   ```bash
   cd /Users/shubhamtiwari/Documents/nullai/customer_service_agent/frontend
   ```

2. **Start React development server**
   ```bash
   npm start
   ```

3. **Verify frontend is running**
   - Browser should automatically open: http://localhost:3000
   - You should see the beautiful Customer Service Agent interface

## 🧪 Testing the System

### Quick Health Check

1. **Backend API Documentation**
   - Open: http://localhost:8000/docs
   - You should see FastAPI's automatic Swagger documentation

2. **Frontend Interface**
   - Open: http://localhost:3000
   - You should see the modern UI with gradient background

### Run Test Suite

In the backend terminal:
```bash
cd /Users/shubhamtiwari/Documents/nullai/customer_service_agent/backend
source venv/bin/activate
python -m pytest test_api.py -v
```
> Should show: `21 passed` - all tests passing ✅

## 🎯 Demo Test Cases

Use these exact inputs in the frontend to test all features:

### 1. Technical Support Query ⚡
**Input:**
```
Query: My password reset isn't working and I can't access my account
Company Name: (leave empty)
Team Size: (leave empty)
```
**Expected Result:**
- Classification: "Technical Support" 
- Sentiment: Neutral 😐
- Solution from knowledge base
- No escalation needed

### 2. Feature Request 🎨
**Input:**
```
Query: Can you add dark mode and mobile app support to your platform?
Company Name: (leave empty)
Team Size: (leave empty)
```
**Expected Result:**
- Classification: "Product Feature Request"
- Professional acknowledgment response
- Request logged to feature_requests.log
- No escalation needed

### 3. Sales Lead - Complete Info 💼
**Input:**
```
Query: I'm interested in your enterprise solution for my company
Company Name: TechCorp
Team Size: 50
```
**Expected Result:**
- Classification: "Sales Lead"
- Personalized response with company name
- Plan recommendation (Professional)
- No escalation needed

### 4. Sales Lead - Missing Info ❓
**Input:**
```
Query: What are your pricing options?
Company Name: (leave empty)
Team Size: (leave empty)
```
**Expected Result:**
- Classification: "Sales Lead"
- Request for missing information
- Escalation triggered (red alert)

### 5. Large Enterprise Lead 🏢
**Input:**
```
Query: We need an enterprise solution for our organization
Company Name: BigCorp Inc
Team Size: 500
```
**Expected Result:**
- Classification: "Sales Lead"
- Enterprise plan recommendation
- Escalation triggered (large team)

### 6. Negative Sentiment Escalation 😟
**Input:**
```
Query: This is terrible! Your service is completely broken and I'm very frustrated with these login issues!
Company Name: (leave empty)
Team Size: (leave empty)
```
**Expected Result:**
- Classification: "Technical Support"
- Sentiment: Negative 😟
- Automatic escalation (red pulse animation)
- Priority support message

### 7. High Confidence Technical 🔧
**Input:**
```
Query: login error problem help issue bug crash broken not working
Company Name: (leave empty)
Team Size: (leave empty)
```
**Expected Result:**
- Classification: "Technical Support"
- High confidence score (>80%)
- Multiple solutions from knowledge base

### 8. Payment Issue 💳
**Input:**
```
Query: My payment method was declined and I can't update my billing information
Company Name: (leave empty)
Team Size: (leave empty)
```
**Expected Result:**
- Classification: "Technical Support"
- Specific payment troubleshooting steps
- No escalation needed

## 🔍 What to Look For

### UI Elements to Notice:
- **Smooth animations** when submitting queries
- **Processing indicators** with bouncing dots
- **Sentiment visualization** with emojis (😊😟😐)
- **Confidence bars** with animated progress
- **Classification badges** with color coding
- **Escalation alerts** with pulse animations
- **Professional styling** with gradients and shadows

### Backend Features:
- **Real-time sentiment analysis** using TextBlob
- **Intelligent classification** based on keywords
- **Knowledge base search** for technical solutions
- **Automatic logging** of feature requests
- **Complex escalation logic** for different scenarios

## 🚨 Troubleshooting

### Backend Issues:
```bash
# If backend won't start
cd backend
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend Issues:
```bash
# If frontend won't start
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

### Port Conflicts:
```bash
# If ports are busy, kill processes
lsof -ti:8000 | xargs kill -9  # Kill backend
lsof -ti:3000 | xargs kill -9  # Kill frontend
```

### CORS Errors:
- Make sure backend is running on port 8000
- Frontend should be on port 3000
- Check browser console for specific errors

## 📊 Expected File Generation

After testing, you should see:
- `backend/feature_requests.log` - Contains logged feature requests
- Various test artifacts in `backend/.pytest_cache/`

## 🎬 Ready for Demo Video

Once everything is working:
1. **Both servers running** (backend: 8000, frontend: 3000)
2. **All test cases working** as described above
3. **No console errors** in browser or terminal
4. **Smooth animations** and professional UI

You're now ready to record your demonstration video following the DEMO_SCRIPT.md!

## 📞 Quick Command Reference

```bash
# Start backend
cd backend && source venv/bin/activate && uvicorn main:app --reload --port 8000

# Start frontend (new terminal)
cd frontend && npm start

# Run tests
cd backend && source venv/bin/activate && python -m pytest test_api.py -v

# Check logs
cat backend/feature_requests.log

# Stop servers
Ctrl+C in each terminal
```

---

🎉 **You now have a fully functional AI-powered customer service agent running locally!**
