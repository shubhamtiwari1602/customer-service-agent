from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from typing import Optional, Literal
import markdown
import datetime
import re
import os
from pathlib import Path
from textblob import TextBlob

app = FastAPI(title="Customer Service Agent API", version="1.0.0")

# Environment-aware CORS configuration
CORS_ORIGINS = [
    "http://localhost:3000",  # Local development
    "http://localhost:3001",  # Alternative local port
    "https://localhost:3000", # Local HTTPS
    "https://customer-service-agent-black.vercel.app",  # Production Vercel
    "https://*.vercel.app",   # All Vercel deployments
    "https://*.github.io",    # GitHub Pages
    "https://*.githubpages.io", # GitHub Pages alternative
    "https://*.netlify.app",  # Netlify deployments
]

# Add production domain if deployed
if os.getenv("PRODUCTION_DOMAIN"):
    CORS_ORIGINS.append(os.getenv("PRODUCTION_DOMAIN"))

# Add CORS middleware with more permissive settings for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if os.getenv("VERCEL") else CORS_ORIGINS,  # Allow all origins on Vercel
    allow_origin_regex=r"https://.*\.(vercel\.app|github\.io|netlify\.app)",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Enhanced knowledge base
KB = {
    "login": "Try resetting your password, clearing browser cache, or checking if cookies are enabled. If the issue persists, verify your account status.",
    "password": "Use the 'Forgot Password' link on the login page. Check your email (including spam folder) for reset instructions.",
    "payment": "Verify your payment method details, check subscription status, or contact billing support at billing@company.com.",
    "billing": "For billing inquiries, please contact our billing team at billing@company.com or check your account settings.",
    "performance": "Clear your browser cache, try a different browser, check your internet connection, or try using incognito mode.",
    "slow": "Performance issues can be resolved by clearing cache, checking internet connection, or trying a different browser.",
    "bug": "Thank you for reporting this bug. Please provide detailed steps to reproduce the issue.",
    "error": "Please provide the exact error message and steps that led to this error for better assistance.",
    "installation": "Follow our installation guide at docs.company.com/install or contact technical support.",
    "api": "Check our API documentation at api.company.com/docs for integration help and examples.",
    "integration": "Visit our integration guide at docs.company.com/integrations for step-by-step instructions.",
}

# Request models
class CustomerQuery(BaseModel):
    query: str
    company_name: Optional[str] = None
    team_size: Optional[int] = None
    
    @field_validator('query')
    @classmethod
    def validate_query(cls, v):
        if not v.strip():
            raise ValueError('Query cannot be empty')
        return v.strip()

class AgentResponse(BaseModel):
    classification: Literal["Technical Support", "Product Feature Request", "Sales Lead"]
    response: str
    needs_escalation: bool
    sentiment: str = "neutral"
    confidence: float = 0.0

def analyze_sentiment(text: str) -> tuple[str, float]:
    """Analyze sentiment using TextBlob"""
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.1:
            sentiment = "positive"
        elif polarity < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"
            
        confidence = abs(polarity)
        return sentiment, confidence
    except:
        return "neutral", 0.0

def classify_query_advanced(text: str) -> tuple[str, float]:
    """Advanced query classification with confidence scoring"""
    text_lower = text.lower()
    
    # Technical support keywords
    tech_keywords = ["help", "issue", "problem", "error", "bug", "crash", "broken", 
                    "not working", "login", "password", "installation", "performance",
                    "slow", "api", "integration", "support"]
    
    # Feature request keywords  
    feature_keywords = ["feature", "request", "suggestion", "improvement", "add",
                       "enhancement", "new", "would like", "could you", "implement",
                       "dark mode", "ui", "ux"]
    
    # Sales keywords
    sales_keywords = ["price", "pricing", "cost", "buy", "purchase", "upgrade",
                     "enterprise", "team", "company", "business", "trial",
                     "demo", "sales", "contact"]
    
    # Count matches
    tech_score = sum(1 for keyword in tech_keywords if keyword in text_lower)
    feature_score = sum(1 for keyword in feature_keywords if keyword in text_lower)
    sales_score = sum(1 for keyword in sales_keywords if keyword in text_lower)
    
    # Determine classification and confidence
    if tech_score >= feature_score and tech_score >= sales_score:
        confidence = min(tech_score / 3.0, 1.0)  # Normalize confidence
        return "Technical Support", confidence
    elif feature_score >= sales_score:
        confidence = min(feature_score / 3.0, 1.0)
        return "Product Feature Request", confidence
    else:
        confidence = min(sales_score / 3.0, 1.0) if sales_score > 0 else 0.3
        return "Sales Lead", confidence

@app.get("/")
async def root():
    return {"message": "Customer Service Agent API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint for deployment monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.post("/classify", response_model=AgentResponse)
async def classify_query(query: CustomerQuery):
    """Classify customer query and generate appropriate response"""
    # Analyze sentiment
    sentiment, sentiment_confidence = analyze_sentiment(query.query)
    
    # Classify query
    classification, confidence = classify_query_advanced(query.query)
    
    # Handle based on classification
    if classification == "Technical Support":
        response, needs_escalation = handle_technical_support(query.query, sentiment)
    elif classification == "Product Feature Request":
        response, needs_escalation = handle_feature_request(query.query)
    else:  # Sales Lead
        response, needs_escalation = handle_sales_lead(query)
    
    # Force escalation for very negative sentiment
    if sentiment == "negative" and sentiment_confidence > 0.5:
        needs_escalation = True
        response += "\n\nNote: Due to the nature of your concern, this has been escalated to our priority support team."

    return AgentResponse(
        classification=classification,
        response=response,
        needs_escalation=needs_escalation,
        sentiment=sentiment,
        confidence=confidence
    )

def handle_technical_support(query: str, sentiment: str = "neutral") -> tuple[str, bool]:
    """Handle technical support queries by searching KB"""
    query_lower = query.lower()
    solutions_found = []
    
    # Search for solutions in KB
    for keyword, solution in KB.items():
        if keyword in query_lower:
            solutions_found.append(solution)
    
    if solutions_found:
        response = "I found the following solution(s):\n\n" + "\n\n".join(solutions_found)
        response += "\n\nIf this doesn't resolve your issue, please let us know!"
        escalation = sentiment == "negative"  # Escalate if negative sentiment
    else:
        response = "I couldn't find a specific solution in our knowledge base. Our technical support team will contact you within 24 hours to assist you personally."
        escalation = True  # Always escalate unknown technical issues
    
    return response, escalation

def handle_feature_request(query: str) -> tuple[str, bool]:
    """Log feature requests to file"""
    log_path = Path("feature_requests.log")
    timestamp = datetime.datetime.now().isoformat()
    
    # Create log file if it doesn't exist
    if not log_path.exists():
        log_path.touch()
    
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"{timestamp}: {query}\n")
    
    response = """Thank you for your feature request! 🚀

Your suggestion has been logged and will be reviewed by our product team. We truly value customer feedback as it helps us improve our product.

You can expect:
- Acknowledgment within 2 business days
- Updates on feature status through our product roadmap
- Priority consideration for highly requested features

Keep the great ideas coming!"""
    
    return response, False

def handle_sales_lead(query: CustomerQuery) -> tuple[str, bool]:
    """Handle sales lead qualification"""
    needs_escalation = False
    missing_info = []
    
    if not query.company_name:
        missing_info.append("company name")
    if not query.team_size:
        missing_info.append("team size")
    
    if missing_info:
        response = f"""Thank you for your interest in our product! 🎯

To provide you with the best pricing and solution recommendations, could you please share your:
{', '.join(missing_info)}

This helps us:
- Customize the perfect plan for your needs
- Provide accurate pricing information  
- Connect you with the right specialist
- Expedite the onboarding process

You can reply with this information or schedule a call with our sales team."""
        needs_escalation = True
    else:
        response = f"""Excellent! Thank you for your interest! 🎉

Company: {query.company_name}
Team Size: {query.team_size}

Based on your team size, I can recommend our {"Enterprise" if query.team_size > 50 else "Professional" if query.team_size > 10 else "Starter"} plan.

Our sales specialist will contact you within 4 hours to:
- Provide a personalized demo
- Discuss pricing options
- Answer any technical questions
- Set up a trial if appropriate

Looking forward to helping {query.company_name} succeed! 🚀"""
        # Escalate large teams for priority handling
        needs_escalation = query.team_size > 100
    
    return response, needs_escalation
