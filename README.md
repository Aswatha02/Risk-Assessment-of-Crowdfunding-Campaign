# 🎯 CrowdRisk - AI-Powered Crowdfunding Risk Assessment

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2+-61DAFB.svg)](https://reactjs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An intelligent machine learning platform that predicts the success probability of crowdfunding campaigns (Kickstarter, Indiegogo, etc.) and provides actionable recommendations to improve campaign outcomes.

## 📋 Table of Contents

- [Features](#-features)
- [Demo](#-demo)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Model Training](#-model-training)
- [Project Structure](#-project-structure)
- [Technologies](#-technologies)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🤖 **AI-Powered Predictions**
- **Ensemble Machine Learning**: Combines Logistic Regression, Decision Tree, and Random Forest models
- **Real-time Risk Assessment**: Instant success probability calculation
- **Feature Importance Analysis**: Understand which factors matter most

### 📊 **Intelligent Insights**
- **Risk Level Classification**: Low/Medium/High risk categorization with color coding
- **Explanatory Analysis**: Human-readable explanations for predictions
- **Actionable Recommendations**: Data-driven suggestions to improve campaign success

### 🎨 **Modern Web Interface**
- **Intuitive Dashboard**: Clean, responsive React UI
- **Interactive Visualizations**: Charts and graphs for model comparisons
- **Real-time Feedback**: Instant results as you input campaign details

### 🔧 **Developer-Friendly**
- **RESTful API**: Well-documented FastAPI backend
- **Swagger Documentation**: Interactive API docs at `/docs`
- **Easy Deployment**: Docker support for containerization
- **Comprehensive Testing**: Unit and integration tests included

## 🎬 Demo

### Input Campaign Details
```
Campaign Name: AI-Powered Smart Watch
Goal: $15,000
Duration: 45 days
Category: Technology
Country: US
```

### Get Instant Predictions
```json
{
  "success_probability": 0.72,
  "risk_level": "Low",
  "recommendations": [
    "Add high-quality images and video to build trust",
    "Promote through social media and email lists"
  ]
}
```

## 🏗️ Architecture

```
┌─────────────────┐      HTTP/REST      ┌──────────────────┐
│  React Frontend │ ◄─────────────────► │  FastAPI Backend │
│   (Port 3000)   │                     │   (Port 8000)    │
└─────────────────┘                     └──────────────────┘
                                                 │
                                                 ▼
                                        ┌──────────────────┐
                                        │  ML Models       │
                                        │  - Logistic Reg  │
                                        │  - Decision Tree │
                                        │  - Random Forest │
                                        └──────────────────┘
```

### **Tech Stack**

**Backend:**
- FastAPI (REST API framework)
- Pandas & NumPy (Data processing)
- Scikit-learn (Machine learning)
- Joblib (Model serialization)

**Frontend:**
- React 18 (UI framework)
- Vite (Build tool)
- Modern CSS (Styling)

**Machine Learning:**
- Custom implementations of ML algorithms
- Feature engineering pipeline
- Target encoding for categorical variables
- Ensemble prediction system

## 🚀 Installation

### Prerequisites

- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Node.js 16+** ([Download](https://nodejs.org/))
- **Git** ([Download](https://git-scm.com/))

### Quick Start

#### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/Risk-Assessment-of-Crowdfunding-Campaign.git
cd Risk-Assessment-of-Crowdfunding-Campaign
```

#### 2️⃣ Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Navigate to backend directory
cd backend/app

# Train the models (required for first-time setup)
python train.py

# Start the API server
python main.py
```

The backend will start at `http://localhost:8000`

#### 3️⃣ Frontend Setup

Open a new terminal:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will start at `http://localhost:3000`

#### 4️⃣ Access the Application

- **Frontend UI**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/health

## 📖 Usage

### Web Interface

1. Open http://localhost:3000 in your browser
2. Fill in campaign details:
   - Campaign name and description
   - Funding goal
   - Campaign duration
   - Category and country
   - Additional metadata
3. Click "Analyze Campaign"
4. View predictions, risk assessment, and recommendations

### API Usage

#### Predict Campaign Success

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AI Smart Watch",
    "blurb": "Revolutionary smart watch with AI assistant",
    "goal": 15000,
    "pledged": 2500,
    "backers_count": 45,
    "country": "US",
    "currency": "USD",
    "category": "Technology",
    "launch_to_deadline_days": 45,
    "staff_pick": true
  }'
```

#### Check API Health

```bash
curl http://localhost:8000/health
```

#### Get Feature Importance

```bash
curl http://localhost:8000/features
```

## 📚 API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint with API info |
| GET | `/health` | Health check and model status |
| POST | `/predict` | Predict campaign success |
| GET | `/features` | Get feature importance |
| GET | `/docs` | Interactive Swagger documentation |

### Request Schema

```json
{
  "name": "string",
  "blurb": "string",
  "goal": 0,
  "pledged": 0,
  "backers_count": 0,
  "country": "US",
  "currency": "USD",
  "category": "Technology",
  "launch_to_deadline_days": 30,
  "create_to_launch_days": 1,
  "staff_pick": false,
  "spotlight": false
}
```

### Response Schema

```json
{
  "success_probability": 0.75,
  "risk_level": "Low",
  "risk_color": "green",
  "model_scores": {
    "logistic_regression": 0.73,
    "decision_tree": 0.76,
    "random_forest": 0.75
  },
  "explanations": [
    "Reasonable funding goal improves chances",
    "Optimal campaign duration for good exposure"
  ],
  "feature_importance": {
    "goal_amount": 0.25,
    "campaign_duration": 0.20
  },
  "recommendations": [
    "Add high-quality images and video",
    "Promote through social media"
  ]
}
```

## 🎓 Model Training

### Training Your Own Models

```bash
cd backend/app
python train.py
```

This will:
1. Load raw data from `data/raw/kickstarter_data_full.csv`
2. Perform feature engineering and preprocessing
3. Train three ML models (Logistic Regression, Decision Tree, Random Forest)
4. Evaluate models on validation and test sets
5. Save trained models to `trained_models/crowdrisk_models.pkl`

### Model Performance

The models are evaluated using:
- **Accuracy**: Overall prediction correctness
- **Precision**: True positive rate
- **Recall**: Sensitivity
- **F1-Score**: Harmonic mean of precision and recall
- **AUC-ROC**: Area under the ROC curve

### Feature Engineering

The pipeline includes:
- Text analysis (name length, description sentiment)
- Temporal features (campaign duration, preparation time)
- Geographic encoding (country success rates)
- Category encoding (category performance)
- Goal analysis (funding target optimization)

## 📁 Project Structure

```
Risk-Assessment-of-Crowdfunding-Campaign/
├── backend/
│   └── app/
│       ├── main.py                 # FastAPI application
│       ├── predict.py              # Prediction logic
│       ├── preprocessing.py        # Data preprocessing
│       ├── train.py                # Model training
│       ├── evaluation.py           # Model evaluation
│       └── models/
│           ├── logistic_regression.py
│           ├── decision_tree.py
│           └── random_forest.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx                # Main React component
│   │   ├── components/            # UI components
│   │   │   ├── InputForm.jsx
│   │   │   ├── ResultsDashboard.jsx
│   │   │   ├── RiskSummaryCard.jsx
│   │   │   ├── ComparisonCharts.jsx
│   │   │   ├── FeatureImportancePlot.jsx
│   │   │   └── Recommendations.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
├── data/
│   ├── raw/                       # Raw Kickstarter data
│   └── processed/                 # Processed datasets
├── trained_models/                # Saved ML models
│   ├── crowdrisk_models.pkl
│   └── feature_names.txt
├── tests/
│   ├── test_api.py               # API integration tests
│   └── test_models.py            # Model unit tests
├── notebooks/
│   └── eda.ipynb                 # Exploratory data analysis
├── requirements.txt              # Python dependencies
├── .gitignore
└── README.md
```

## 🛠️ Technologies

### Backend
- **FastAPI** - Modern, fast web framework
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Scikit-learn** - Machine learning utilities
- **Joblib** - Model persistence
- **Uvicorn** - ASGI server

### Frontend
- **React** - UI library
- **Vite** - Build tool and dev server
- **Modern CSS** - Styling

### Machine Learning
- **Logistic Regression** - Binary classification
- **Decision Tree** - Non-linear patterns
- **Random Forest** - Ensemble learning

## 🧪 Testing

### Run Backend Tests

```bash
cd tests
python test_api.py
python test_models.py
```

### Run Frontend Tests

```bash
cd frontend
npm test
```
