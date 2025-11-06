# 🚀 CrowdRisk Quick Start Guide

Get up and running with CrowdRisk in 5 minutes!

## ⚡ Quick Setup (Automated)

### Windows
```bash
# Run the automated setup
python setup.py

# Start the application
start.bat
```

### Linux/Mac
```bash
# Run the automated setup
python3 setup.py

# Make start script executable
chmod +x start.sh

# Start the application
./start.sh
```

## 📋 Manual Setup

### Step 1: Install Dependencies

**Backend:**
```bash
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### Step 2: Train Models (First Time Only)

```bash
cd backend/app
python train.py
```

⏱️ This takes 5-10 minutes depending on your machine.

### Step 3: Start Servers

**Terminal 1 - Backend:**
```bash
cd backend/app
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## 🌐 Access the Application

- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🧪 Test the API

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Campaign",
    "blurb": "This is a test campaign",
    "goal": 10000,
    "country": "US",
    "category": "Technology",
    "launch_to_deadline_days": 30
  }'
```

## 🐳 Docker Setup (Alternative)

```bash
# Build and start
docker-compose up --build

# Access at:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

## 📊 Using the Web Interface

1. Open http://localhost:3000
2. Fill in campaign details:
   - **Name**: Your campaign name
   - **Description**: Brief campaign description
   - **Goal**: Funding target (e.g., 15000)
   - **Duration**: Campaign length in days (e.g., 30)
   - **Category**: Select from dropdown
   - **Country**: Select your country
3. Click **"Analyze Campaign"**
4. View results:
   - Success probability
   - Risk level
   - Recommendations

## 🔧 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
# Windows:
netstat -ano | findstr :8000

# Linux/Mac:
lsof -i :8000

# Kill the process or use a different port
```

### Frontend won't start
```bash
# Check if port 3000 is in use
# Windows:
netstat -ano | findstr :3000

# Linux/Mac:
lsof -i :3000

# Delete node_modules and reinstall
cd frontend
rm -rf node_modules
npm install
```

### Models not loading
```bash
# Retrain the models
cd backend/app
python train.py

# Check if models file exists
ls ../../trained_models/crowdrisk_models.pkl
```

### CORS errors
- Make sure backend is running on port 8000
- Make sure frontend is running on port 3000
- Check browser console for specific errors

## 📚 Next Steps

- Read the [Full Documentation](README.md)
- Check the [API Documentation](API.md)
- Explore [Contributing Guidelines](CONTRIBUTING.md)
- Run the [Tests](tests/)

## 💡 Tips

1. **First time?** Run `python setup.py` for automated setup
2. **Development?** Use `start.bat` (Windows) or `start.sh` (Linux/Mac)
3. **Production?** Use Docker with `docker-compose up`
4. **Testing?** The API works even without trained models (fallback mode)

## ❓ Common Questions

**Q: Do I need the Kickstarter dataset?**  
A: Only if you want to train models. The app works in fallback mode without it.

**Q: How long does training take?**  
A: 5-10 minutes on a modern laptop.

**Q: Can I use my own data?**  
A: Yes! Place your CSV in `data/raw/` and update the path in `train.py`.

**Q: Is this production-ready?**  
A: It's a demo/prototype. Add authentication, rate limiting, and monitoring for production.

## 🆘 Getting Help

- Check [README.md](README.md) for detailed docs
- Open an issue on GitHub
- Check existing issues for solutions

---

**Ready to assess some campaigns? Let's go! 🎯**
