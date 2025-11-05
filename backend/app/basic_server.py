from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import math
import random

class CrowdRiskAPI(BaseHTTPRequestHandler):
    
    def _set_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()
    
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self._set_cors_headers()
            self.end_headers()
            
            response = {
                "status": "healthy",
                "message": "CrowdRisk API Server",
                "version": "1.0.0",
                "mode": "dependency_free"
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self._set_cors_headers()
            self.end_headers()
            
            response = {
                "message": "🚀 CrowdRisk API - AI Crowdfunding Risk Assessment",
                "endpoints": {
                    "health": "/health",
                    "predict": "/predict (POST)"
                }
            }
            self.wfile.write(json.dumps(response).encode())
            
        else:
            self.send_response(404)
            self._set_cors_headers()
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/predict':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data)
                
                print(f"📨 Received prediction request for: {data.get('name', 'Unknown')}")
                
                # Calculate prediction
                result = self.calculate_prediction(data)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self._set_cors_headers()
                self.end_headers()
                
                self.wfile.write(json.dumps(result).encode())
                print(f"✅ Prediction completed: {result['success_probability']:.1%} success")
                
            except Exception as e:
                print(f"❌ Error: {e}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self._set_cors_headers()
                self.end_headers()
                error_response = {"error": str(e)}
                self.wfile.write(json.dumps(error_response).encode())
        else:
            self.send_response(404)
            self._set_cors_headers()
            self.end_headers()
    
    def calculate_prediction(self, data):
        """Calculate intelligent prediction using only Python built-ins"""
        goal = data.get('goal', 0)
        duration = data.get('launch_to_deadline_days', 30)
        country = data.get('country', 'US')
        category = data.get('category', 'Technology')
        staff_pick = data.get('staff_pick', False)
        pledged = data.get('pledged', 0)
        backers = data.get('backers_count', 0)
        blurb = data.get('blurb', '')
        name = data.get('name', 'Unknown Project')
        
        # Smart probability calculation without numpy
        goal_factor = max(0.1, 1.0 - min(goal / 50000, 1.0))
        duration_factor = 1.0 if 30 <= duration <= 45 else 0.7
        country_factor = 1.2 if country in ['US', 'GB'] else 1.0
        category_factor = 1.1 if category in ['Technology', 'Games', 'Design'] else 1.0
        staff_factor = 1.3 if staff_pick else 1.0
        funding_ratio = min(pledged / max(goal, 1), 2.0)
        backer_factor = min(backers / 50, 2.0)
        description_factor = min(len(blurb) / 100, 1.5)
        
        # Combine factors
        base_prob = 0.35
        success_prob = (base_prob * goal_factor * duration_factor * 
                       country_factor * category_factor * staff_factor)
        success_prob += (funding_ratio * 0.15 + backer_factor * 0.1 + 
                        description_factor * 0.05)
        
        # Ensure reasonable bounds
        success_prob = max(0.05, min(0.95, success_prob))
        
        # Model variations (simulate ensemble without numpy)
        model_scores = {
            'logistic_regression': success_prob * 0.96,
            'decision_tree': success_prob * 1.04,
            'random_forest': success_prob
        }
        
        # Calculate average without numpy
        avg_prob = sum(model_scores.values()) / len(model_scores)
        
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
        
        # Normalize importance scores without numpy
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

def main():
    port = 8000
    server = HTTPServer(('localhost', port), CrowdRiskAPI)
    
    print("🚀 CrowdRisk API Server Starting...")
    print(f"📍 http://localhost:{port}")
    print("📊 100% Dependency-Free Python")
    print("🔗 CORS Enabled for Frontend")
    print("🎯 Ready for predictions!")
    print("-" * 50)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        server.socket.close()

if __name__ == '__main__':
    main()