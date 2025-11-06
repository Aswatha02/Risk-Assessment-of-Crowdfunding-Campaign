# CrowdRisk API Documentation

Complete API reference for the CrowdRisk backend service.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. This may be added in future versions.

## Endpoints

### 1. Root Endpoint

Get basic API information.

**Endpoint:** `GET /`

**Response:**
```json
{
  "message": "🎯 CrowdRisk API - Intelligent Crowdfunding Risk Assessment",
  "status": "healthy",
  "mode": "production",
  "version": "1.0.0",
  "models_loaded": true
}
```

**Fields:**
- `message` (string): Welcome message
- `status` (string): API status
- `mode` (string): "production" if models loaded, "fallback" otherwise
- `version` (string): API version
- `models_loaded` (boolean): Whether ML models are loaded

---

### 2. Health Check

Check API health and model status.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "mode": "production",
  "models_loaded": true,
  "total_features": 85,
  "cors_enabled": true,
  "endpoints": ["/", "/health", "/predict", "/features", "/docs"],
  "metadata": {
    "training_date": "2024-11-06 21:00:00",
    "dataset_shape": "50000 samples, 85 features",
    "class_distribution": "Success: 35.62%, Fail: 64.38%",
    "models_trained": ["Logistic Regression", "Decision Tree", "Random Forest"]
  }
}
```

**Fields:**
- `status` (string): Health status
- `mode` (string): Operation mode
- `models_loaded` (boolean): Model availability
- `total_features` (integer): Number of features used
- `metadata` (object): Training information (if models loaded)

---

### 3. Predict Campaign Success

Predict the success probability of a crowdfunding campaign.

**Endpoint:** `POST /predict`

**Request Body:**
```json
{
  "name": "AI-Powered Smart Watch",
  "blurb": "Revolutionary smart watch with AI assistant and health monitoring",
  "goal": 15000,
  "pledged": 2500,
  "backers_count": 45,
  "country": "US",
  "currency": "USD",
  "category": "Technology",
  "launch_to_deadline_days": 45,
  "create_to_launch_days": 7,
  "staff_pick": true,
  "spotlight": false
}
```

**Request Fields:**

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `name` | string | Yes | - | Campaign name |
| `blurb` | string | Yes | - | Campaign description |
| `goal` | float | Yes | - | Funding goal in currency units |
| `pledged` | float | No | 0 | Amount already pledged |
| `backers_count` | integer | No | 0 | Number of backers |
| `country` | string | No | "US" | Country code (ISO 2-letter) |
| `currency` | string | No | "USD" | Currency code (ISO 3-letter) |
| `category` | string | No | "Technology" | Campaign category |
| `launch_to_deadline_days` | integer | No | 30 | Campaign duration in days |
| `create_to_launch_days` | integer | No | 1 | Preparation time in days |
| `staff_pick` | boolean | No | false | Whether campaign is staff picked |
| `spotlight` | boolean | No | false | Whether campaign is spotlighted |

**Response:**
```json
{
  "success_probability": 0.7234,
  "risk_level": "Low",
  "risk_color": "green",
  "model_scores": {
    "logistic_regression": 0.7156,
    "decision_tree": 0.7289,
    "random_forest": 0.7258
  },
  "explanations": [
    "Reasonable funding goal improves chances",
    "Optimal campaign duration for good exposure",
    "Strong crowdfunding market with high success rates",
    "Staff pick status greatly increases visibility and trust"
  ],
  "feature_importance": {
    "goal_amount": 0.28,
    "campaign_duration": 0.22,
    "country": 0.18,
    "staff_pick": 0.17,
    "early_funding": 0.15
  },
  "recommendations": [
    "Add high-quality images and video to build trust",
    "Promote through social media and email lists"
  ]
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `success_probability` | float | Overall success probability (0-1) |
| `risk_level` | string | "Low", "Medium", or "High" |
| `risk_color` | string | Color code: "green", "orange", or "red" |
| `model_scores` | object | Individual model predictions |
| `explanations` | array | Human-readable explanations |
| `feature_importance` | object | Feature importance scores |
| `recommendations` | array | Actionable recommendations |

**Risk Levels:**
- **Low Risk** (>70% probability): Green
- **Medium Risk** (40-70% probability): Orange
- **High Risk** (<40% probability): Red

**Status Codes:**
- `200 OK`: Successful prediction
- `422 Unprocessable Entity`: Invalid request data
- `500 Internal Server Error`: Prediction error

---

### 4. Get Feature Information

Get information about features used in the model.

**Endpoint:** `GET /features`

**Response:**
```json
{
  "total_features": 85,
  "feature_names": [
    "goal_usd",
    "pledged_usd",
    "backers_count",
    "launch_to_deadline_days",
    "...more features..."
  ],
  "top_10_features": [
    "goal_usd",
    "pledged_usd",
    "backers_count",
    "launch_to_deadline_days",
    "staff_pick",
    "category_te",
    "country_te",
    "blurb_len",
    "name_len",
    "text_sentiment_score"
  ],
  "feature_importance": {
    "goal_usd": 0.1523,
    "pledged_usd": 0.1289,
    "backers_count": 0.1156,
    "launch_to_deadline_days": 0.0987,
    "staff_pick": 0.0876,
    "category_te": 0.0754,
    "country_te": 0.0698,
    "blurb_len": 0.0543,
    "name_len": 0.0432,
    "text_sentiment_score": 0.0389
  }
}
```

**Status Codes:**
- `200 OK`: Features retrieved successfully
- `503 Service Unavailable`: Models not loaded

---

## Interactive Documentation

FastAPI provides interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## CORS Configuration

The API allows requests from:
- `http://localhost:3000`
- `http://127.0.0.1:3000`
- `http://localhost:8000`
- `http://127.0.0.1:8000`

## Error Handling

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

**Common Error Codes:**
- `400 Bad Request`: Invalid input
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: Service not ready

## Rate Limiting

Currently, there is no rate limiting. This may be added in future versions.

## Examples

### cURL Examples

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Predict Campaign:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Smart Garden System",
    "blurb": "Automated indoor garden with IoT sensors",
    "goal": 25000,
    "country": "US",
    "category": "Technology",
    "launch_to_deadline_days": 30
  }'
```

### Python Examples

```python
import requests

# Health check
response = requests.get("http://localhost:8000/health")
print(response.json())

# Predict campaign
campaign = {
    "name": "Smart Garden System",
    "blurb": "Automated indoor garden with IoT sensors",
    "goal": 25000,
    "country": "US",
    "category": "Technology",
    "launch_to_deadline_days": 30
}

response = requests.post(
    "http://localhost:8000/predict",
    json=campaign
)
result = response.json()
print(f"Success Probability: {result['success_probability']:.2%}")
print(f"Risk Level: {result['risk_level']}")
```

### JavaScript Examples

```javascript
// Health check
fetch('http://localhost:8000/health')
  .then(response => response.json())
  .then(data => console.log(data));

// Predict campaign
const campaign = {
  name: "Smart Garden System",
  blurb: "Automated indoor garden with IoT sensors",
  goal: 25000,
  country: "US",
  category: "Technology",
  launch_to_deadline_days: 30
};

fetch('http://localhost:8000/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(campaign)
})
  .then(response => response.json())
  .then(data => {
    console.log(`Success Probability: ${(data.success_probability * 100).toFixed(2)}%`);
    console.log(`Risk Level: ${data.risk_level}`);
  });
```

## Versioning

Current version: **1.0.0**

The API follows semantic versioning. Breaking changes will increment the major version.

## Support

For issues or questions:
- GitHub Issues: [Repository Issues](https://github.com/yourusername/Risk-Assessment-of-Crowdfunding-Campaign/issues)
- Documentation: [README.md](README.md)

---

**Last Updated:** November 2024
