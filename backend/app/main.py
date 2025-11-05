from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import pandas as pd
import numpy as np
import uvicorn

app = FastAPI(
    title="CrowdRisk API",
    description="AI-Powered Crowdfunding Risk Assessment",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enhanced CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://127.0.0.1:3000",  # Alternative localhost
        "http://localhost:8000",  # Backend itself
        "http://127.0.0.1:8000",  # Alternative backend
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"]  # Expose all headers
)

class CampaignData(BaseModel):
    name: str
    blurb: str
    goal: float
    pledged: float = 0
    backers_count: int = 0
    country: str = "US"
    currency: str = "USD"
    category: str = "Technology"
    launch_to_deadline_days: int = 30
    create_to_launch_days: int = 1
    staff_pick: bool = False
    spotlight: bool = False

class PredictionResponse(BaseModel):
    success_probability: float
    risk_level: str
    risk_color: str
    model_scores: Dict[str, float]
    explanations: List[str]
    feature_importance: Dict[str, float]
    recommendations: List[str]

def smart_predict_campaign(campaign_data: Dict) -> Dict[str, Any]:
    """Intelligent mock prediction based on campaign data"""
    goal = campaign_data.get('goal', 0)
    duration = campaign_data.get('launch_to_deadline_days', 30)
    country = campaign_data.get('country', 'US')
    category = campaign_data.get('category', 'Technology')
    staff_pick = campaign_data.get('staff_pick', False)
    pledged = campaign_data.get('pledged', 0)
    backers = campaign_data.get('backers_count', 0)
    blurb_length = len(campaign_data.get('blurb', ''))
    
    # Calculate base probability with realistic rules
    goal_factor = max(0.1, 1.0 - (goal / 100000))
    duration_factor = 1.0 if 30 <= duration <= 45 else 0.7
    country_factor = 1.2 if country in ['US', 'GB'] else 1.0
    category_factor = 1.1 if category in ['Technology', 'Games', 'Design'] else 1.0
    staff_factor = 1.3 if staff_pick else 1.0
    pledge_ratio = min(pledged / (goal + 1), 2.0)
    backer_factor = min(backers / 100, 2.0)
    blurb_factor = min(blurb_length / 100, 1.5)
    
    # Combine factors
    base_prob = 0.3
    adjusted_prob = base_prob * goal_factor * duration_factor * country_factor * category_factor * staff_factor
    adjusted_prob += (pledge_ratio * 0.2) + (backer_factor * 0.15) + (blurb_factor * 0.1)
    
    success_prob = max(0.05, min(0.95, adjusted_prob))
    
    # Model scores with realistic variations
    model_scores = {
        'logistic_regression': success_prob * 0.95,
        'decision_tree': success_prob * 1.05, 
        'random_forest': success_prob
    }
    
    avg_prob = np.mean(list(model_scores.values()))
    
    # Risk level
    if avg_prob > 0.7:
        risk_level = "Low"
        risk_color = "green"
    elif avg_prob > 0.4:
        risk_level = "Medium"
        risk_color = "orange"
    else:
        risk_level = "High"
        risk_color = "red"
    
    # Intelligent explanations
    explanations = []
    if goal > 50000:
        explanations.append("Very high funding goal significantly increases risk")
    elif goal > 20000:
        explanations.append("High funding goal may be challenging")
    else:
        explanations.append("Reasonable funding goal improves chances")
    
    if duration < 21:
        explanations.append("Very short campaign duration limits exposure")
    elif duration > 60:
        explanations.append("Long campaign duration may reduce urgency")
    else:
        explanations.append("Optimal campaign duration for good exposure")
    
    if country in ['US', 'GB']:
        explanations.append("Strong crowdfunding market with high success rates")
    elif country in ['CA', 'AU', 'DE']:
        explanations.append("Good international crowdfunding presence")
    
    if staff_pick:
        explanations.append("Staff pick status greatly increases visibility and trust")
    
    # Smart recommendations
    recommendations = []
    if goal > 50000 and avg_prob < 0.6:
        recommendations.append("Consider reducing goal to $20,000-$30,000 range")
    if duration < 30:
        recommendations.append("Extend campaign to 30-45 days for optimal reach")
    if blurb_length < 150:
        recommendations.append("Expand project description to 200+ characters")
    if not staff_pick:
        recommendations.append("Focus on quality content to get staff pick status")
    
    if len(recommendations) < 2:
        recommendations.extend([
            "Add high-quality images and video to build trust",
            "Promote through social media and email lists"
        ])
    
    # Feature importance
    feature_importance = {
        "goal_amount": min(goal / 50000, 1.0),
        "campaign_duration": 0.8 if 30 <= duration <= 45 else 0.4,
        "country": 0.7 if country in ['US', 'GB'] else 0.3,
        "staff_pick": 0.9 if staff_pick else 0.1,
        "early_funding": min(pledged / (goal + 1), 1.0)
    }
    
    # Normalize
    total = sum(feature_importance.values())
    if total > 0:
        feature_importance = {k: v/total for k, v in feature_importance.items()}
    
    return {
        "success_probability": float(avg_prob),
        "risk_level": risk_level,
        "risk_color": risk_color,
        "model_scores": {k: float(v) for k, v in model_scores.items()},
        "explanations": explanations[:5],
        "feature_importance": feature_importance,
        "recommendations": recommendations[:4]
    }

@app.get("/")
async def root():
    return {
        "message": "🎯 CrowdRisk API - Intelligent Crowdfunding Risk Assessment",
        "status": "healthy", 
        "mode": "smart_demo",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "mode": "smart_demo",
        "cors_enabled": True,
        "endpoints": ["/", "/health", "/predict", "/docs"]
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict_risk(campaign: CampaignData):
    """Predict success probability for a campaign"""
    try:
        print(f"📨 Received prediction request for: {campaign.name}")
        campaign_dict = campaign.dict()
        result = smart_predict_campaign(campaign_dict)
        print(f"✅ Prediction completed: {result['success_probability']:.2%} success chance")
        return PredictionResponse(**result)
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

# Add CORS preflight options handler
@app.options("/{rest_of_path:path}")
async def preflight_handler():
    return {}

@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

if __name__ == "__main__":
    print("🚀 Starting CrowdRisk API Server on http://localhost:8000")
    print("📊 CORS enabled for: http://localhost:3000")
    print("🔗 Frontend should connect from: http://localhost:3000")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)