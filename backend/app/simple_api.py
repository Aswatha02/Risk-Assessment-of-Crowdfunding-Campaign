from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import numpy as np

app = FastAPI(
    title="CrowdRisk API",
    description="AI-Powered Crowdfunding Risk Assessment",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

def calculate_smart_prediction(campaign_data: Dict) -> Dict[str, Any]:
    """Calculate intelligent predictions based on campaign data"""
    goal = campaign_data.get('goal', 0)
    duration = campaign_data.get('launch_to_deadline_days', 30)
    country = campaign_data.get('country', 'US')
    category = campaign_data.get('category', 'Technology')
    staff_pick = campaign_data.get('staff_pick', False)
    pledged = campaign_data.get('pledged', 0)
    backers = campaign_data.get('backers_count', 0)
    blurb = campaign_data.get('blurb', '')
    
    # Smart probability calculation
    goal_score = max(0.1, 1.0 - min(goal / 50000, 1.0))
    duration_score = 1.0 if 30 <= duration <= 45 else 0.7
    country_score = 1.2 if country in ['US', 'GB'] else 1.0
    category_score = 1.1 if category in ['Technology', 'Games', 'Design'] else 1.0
    staff_score = 1.3 if staff_pick else 1.0
    funding_ratio = min(pledged / max(goal, 1), 2.0)
    backer_score = min(backers / 50, 2.0)
    description_score = min(len(blurb) / 100, 1.5)
    
    # Combine factors
    base_success = 0.35
    success_prob = base_success * goal_score * duration_score * country_score * category_score * staff_score
    success_prob += funding_ratio * 0.15 + backer_score * 0.1 + description_score * 0.05
    
    # Ensure reasonable bounds
    success_prob = max(0.05, min(0.95, success_prob))
    
    # Model variations
    model_scores = {
        'logistic_regression': success_prob * 0.96,
        'decision_tree': success_prob * 1.04,
        'random_forest': success_prob
    }
    
    avg_prob = np.mean(list(model_scores.values()))
    
    # Risk assessment
    if avg_prob > 0.7:
        risk_level = "Low"
        risk_color = "green"
    elif avg_prob > 0.4:
        risk_level = "Medium"
        risk_color = "orange"
    else:
        risk_level = "High"
        risk_color = "red"
    
    # Generate intelligent explanations
    explanations = []
    
    if goal > 50000:
        explanations.append("Very high funding goal significantly increases risk")
    elif goal > 20000:
        explanations.append("High funding goal may be challenging to reach")
    else:
        explanations.append("Reasonable funding goal improves success chances")
    
    if duration < 21:
        explanations.append("Very short campaign duration limits audience reach")
    elif duration > 60:
        explanations.append("Long campaign duration may reduce backer urgency")
    else:
        explanations.append("Optimal campaign duration for maximum exposure")
    
    if country in ['US', 'GB']:
        explanations.append("Strong crowdfunding market with proven success rates")
    elif country in ['CA', 'AU', 'DE']:
        explanations.append("Established international crowdfunding presence")
    
    if staff_pick:
        explanations.append("Staff pick status provides significant visibility boost")
    
    if pledged > goal * 0.3:
        explanations.append("Strong early funding indicates good campaign momentum")
    
    # Actionable recommendations
    recommendations = []
    
    if goal > 40000 and avg_prob < 0.6:
        recommendations.append("Consider reducing goal to $15,000-$25,000 range")
    
    if duration < 25:
        recommendations.append("Extend campaign to 30-45 days for better reach")
    elif duration > 60:
        recommendations.append("Shorten campaign to 30-45 days to create urgency")
    
    if len(blurb) < 120:
        recommendations.append("Expand project description to 150+ characters with key benefits")
    
    if not staff_pick:
        recommendations.append("Focus on high-quality content and updates to earn staff pick")
    
    if len(recommendations) < 3:
        recommendations.extend([
            "Include high-quality images and video to build trust",
            "Promote through social media and email newsletters",
            "Plan regular updates to keep backers engaged"
        ])
    
    # Feature importance
    feature_importance = {
        "goal_amount": min(goal / 40000, 1.0),
        "campaign_duration": 0.8 if 30 <= duration <= 45 else 0.4,
        "country": 0.7 if country in ['US', 'GB'] else 0.3,
        "staff_pick": 0.9 if staff_pick else 0.1,
        "early_funding": min(pledged / max(goal, 1), 1.0),
        "category": 0.6 if category in ['Technology', 'Games'] else 0.4
    }
    
    # Normalize importance scores
    total = sum(feature_importance.values())
    if total > 0:
        feature_importance = {k: round(v/total, 3) for k, v in feature_importance.items()}
    
    return {
        "success_probability": round(avg_prob, 4),
        "risk_level": risk_level,
        "risk_color": risk_color,
        "model_scores": {k: round(v, 4) for k, v in model_scores.items()},
        "explanations": explanations[:5],
        "feature_importance": feature_importance,
        "recommendations": recommendations[:4]
    }

@app.get("/")
async def root():
    return {
        "message": "🚀 CrowdRisk API - AI Crowdfunding Risk Assessment",
        "status": "healthy",
        "version": "1.0.0",
        "mode": "smart_demo"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "models": "smart_rule_based",
        "endpoints": ["/", "/health", "/predict", "/docs"]
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict_risk(campaign: CampaignData):
    """Predict campaign success probability"""
    try:
        print(f"🎯 Predicting for: {campaign.name}")
        result = calculate_smart_prediction(campaign.dict())
        print(f"✅ Success probability: {result['success_probability']:.1%}")
        return PredictionResponse(**result)
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting CrowdRisk API Server...")
    print("📍 http://localhost:8000")
    print("📊 Smart rule-based predictions enabled")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)