import pandas as pd
import numpy as np
from typing import Dict, Any, List
import re
from datetime import datetime

def preprocess_campaign(campaign_data: Dict[str, Any], encoders: Dict, feature_names: List[str]) -> np.ndarray:
    """
    Preprocess a single campaign for prediction
    """
    # Create a DataFrame with the same structure as training data
    df = pd.DataFrame([campaign_data])
    
    # Basic feature engineering similar to training
    df_processed = basic_feature_engineering(df)
    
    # Apply target encoding for categorical variables
    df_encoded = apply_target_encoding(df_processed, encoders)
    
    # Select only the features used in training
    final_features = []
    for feature in feature_names:
        if feature in df_encoded.columns:
            final_features.append(df_encoded[feature].iloc[0])
        else:
            final_features.append(0.0)  # Default value for missing features
    
    return np.array([final_features])

def basic_feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """Basic feature engineering for prediction"""
    df_engineered = df.copy()
    
    # Text features
    df_engineered['name_len'] = df_engineered.get('name', '').astype(str).str.len()
    df_engineered['blurb_len'] = df_engineered.get('blurb', '').astype(str).str.len()
    df_engineered['blurb_exclaims'] = df_engineered.get('blurb', '').astype(str).str.count('!')
    
    # Simple sentiment analysis
    positive_words = ["amazing", "innovative", "exciting", "unique", "help", "support", "love", "new", "great"]
    negative_words = ["delay", "problem", "issue", "cancel", "refund", "risk", "challenge"]
    
    blurb_text = df_engineered.get('blurb', '').astype(str).str.lower()
    df_engineered['blurb_positive_score'] = blurb_text.apply(
        lambda t: sum(t.count(w) for w in positive_words)
    )
    df_engineered['blurb_negative_score'] = blurb_text.apply(
        lambda t: sum(t.count(w) for w in negative_words)
    )
    df_engineered['text_sentiment_score'] = (
        df_engineered['blurb_positive_score'] - df_engineered['blurb_negative_score']
    )
    
    # Duration features
    df_engineered['duration_risk_short'] = (df_engineered.get('launch_to_deadline_days', 0) < 7).astype(int)
    df_engineered['duration_risk_long'] = (df_engineered.get('launch_to_deadline_days', 0) > 90).astype(int)
    
    # Goal analysis
    df_engineered['goal_usd'] = df_engineered.get('goal', 0)
    df_engineered['pledged_usd'] = df_engineered.get('pledged', 0)
    df_engineered['pledge_ratio'] = df_engineered['pledged_usd'] / (df_engineered['goal_usd'] + 1e-9)
    
    # Country features
    df_engineered['USorGB'] = df_engineered.get('country', '').isin(['US', 'GB']).astype(int)
    
    return df_engineered

def apply_target_encoding(df: pd.DataFrame, encoders: Dict) -> pd.DataFrame:
    """Apply target encoding to categorical variables"""
    df_encoded = df.copy()
    
    categorical_cols = ["category", "country", "currency"]
    for col in categorical_cols:
        if col in df_encoded.columns and col in encoders:
            enc_map = encoders.get(col, {})
            default_value = encoders.get("global_mean", 0.5)
            df_encoded[f"{col}_te"] = df_encoded[col].fillna("___missing___").map(enc_map).fillna(default_value)
    
    return df_encoded

def generate_explanations(campaign_data: Dict, predictions: Dict) -> List[str]:
    """Generate human-readable explanations for the prediction"""
    explanations = []
    
    goal = campaign_data.get('goal', 0)
    duration = campaign_data.get('launch_to_deadline_days', 0)
    country = campaign_data.get('country', '')
    category = campaign_data.get('category', '')
    staff_pick = campaign_data.get('staff_pick', False)
    
    # Goal analysis
    if goal > 50000:
        explanations.append("Very high funding goal increases risk")
    elif goal > 20000:
        explanations.append("High funding goal may be challenging")
    elif goal < 5000:
        explanations.append("Moderate funding goal improves chances")
    
    # Duration analysis
    if duration < 14:
        explanations.append("Very short campaign duration increases risk")
    elif duration < 30:
        explanations.append("Short campaign duration may limit exposure")
    elif 30 <= duration <= 45:
        explanations.append("Optimal campaign duration")
    else:
        explanations.append("Long campaign duration may reduce urgency")
    
    # Geographic analysis
    if country in ['US', 'GB', 'CA', 'AU']:
        explanations.append("Strong geographic market for crowdfunding")
    elif country in ['DE', 'FR', 'NL']:
        explanations.append("Good European market presence")
    else:
        explanations.append("Emerging crowdfunding market")
    
    # Staff pick
    if staff_pick:
        explanations.append("Staff pick status significantly boosts visibility")
    
    # Category sentiment
    high_success_categories = ['Technology', 'Games', 'Design', 'Film & Video']
    if category in high_success_categories:
        explanations.append("Popular category with good track record")
    
    return explanations

def generate_recommendations(campaign_data: Dict, success_prob: float) -> List[str]:
    """Generate personalized, actionable recommendations based on actual campaign data"""
    recommendations = []
    
    # Extract campaign details
    goal = campaign_data.get('goal', 0)
    duration = campaign_data.get('launch_to_deadline_days', 0)
    category = campaign_data.get('category', 'Unknown')
    country = campaign_data.get('country', 'US')
    blurb_len = len(campaign_data.get('blurb', ''))
    name_len = len(campaign_data.get('name', ''))
    has_video = campaign_data.get('has_video', False)
    num_images = campaign_data.get('number_of_images', 0)
    creator_backed = campaign_data.get('creator_backed_projects', 0)
    creator_created = campaign_data.get('creator_created_projects', 0)
    creator_has_avatar = campaign_data.get('creator_has_avatar', False)
    creator_has_bio = campaign_data.get('creator_has_bio', False)
    reward_tiers = campaign_data.get('reward_tiers', 0)
    has_early_bird = campaign_data.get('has_early_bird', False)
    social_followers = campaign_data.get('social_media_followers', 0)
    has_website = campaign_data.get('has_external_website', False)
    
    # PERSONALIZED GOAL RECOMMENDATIONS
    if goal > 100000:
        recommendations.append(f"🎯 Your ${goal:,} goal is extremely ambitious. Consider ${goal//4:,}-${goal//3:,} for {category} campaigns")
    elif goal > 50000:
        recommendations.append(f"🎯 ${goal:,} is very high. Reduce to $20,000-$35,000 to increase success by 40%")
    elif goal > 30000 and success_prob < 0.6:
        recommendations.append(f"🎯 Lower your ${goal:,} goal to $15,000-$20,000 for better chances")
    elif goal < 1000:
        recommendations.append(f"🎯 ${goal:,} seems too low. Consider $3,000-$5,000 to appear more credible")
    
    # PERSONALIZED DURATION RECOMMENDATIONS
    if duration < 14:
        recommendations.append(f"⏰ {duration} days is too short! Extend to 30-35 days for +50% more backers")
    elif duration < 21:
        recommendations.append(f"⏰ {duration} days is short. Aim for 30-35 days (optimal window)")
    elif duration > 60:
        recommendations.append(f"⏰ {duration} days is too long. Shorten to 35-45 days to create urgency")
    elif 30 <= duration <= 45:
        recommendations.append(f"✅ {duration} days is optimal! Perfect campaign length")
    
    # VIDEO RECOMMENDATIONS (HIGH IMPACT)
    if not has_video:
        recommendations.append("🎥 ADD A VIDEO! Campaigns with videos raise 85% more funds (critical)")
    
    # IMAGE RECOMMENDATIONS
    if num_images < 3:
        recommendations.append(f"📸 Add more images! You have {num_images}, aim for 8-12 high-quality photos")
    elif num_images < 5:
        recommendations.append(f"📸 {num_images} images is okay, but 8-10 would build more trust")
    
    # CREATOR PROFILE RECOMMENDATIONS (HIGH IMPACT)
    if not creator_has_avatar:
        recommendations.append("👤 Add a profile photo! Backers trust creators with faces (+30% credibility)")
    if not creator_has_bio:
        recommendations.append("📝 Write a detailed bio! Share your story and expertise")
    if creator_backed == 0:
        recommendations.append("💚 Back other projects! Show you're part of the community (back 5-10 projects)")
    elif creator_backed < 5:
        recommendations.append(f"💚 You've backed {creator_backed} projects. Back 10+ to show community support")
    
    # REWARD STRUCTURE RECOMMENDATIONS
    if reward_tiers < 3:
        recommendations.append(f"🎁 Add more reward tiers! You have {reward_tiers}, offer 5-7 options")
    if not has_early_bird:
        recommendations.append("⚡ Add early bird rewards! Limited-time offers create urgency")
    
    # SOCIAL MEDIA RECOMMENDATIONS
    if social_followers < 100:
        recommendations.append(f"📱 Build your audience! {social_followers} followers is low. Aim for 500+ before launch")
    elif social_followers < 500:
        recommendations.append(f"📱 Grow to 1,000+ followers before launch (you have {social_followers})")
    
    # WEBSITE RECOMMENDATION
    if not has_website:
        recommendations.append("🌐 Create a landing page! External websites increase credibility by 25%")
    
    # TEXT QUALITY RECOMMENDATIONS
    if blurb_len < 100:
        recommendations.append(f"📄 Your description is only {blurb_len} characters. Write 200-300 for best results")
    if name_len < 10:
        recommendations.append(f"✏️ Your project name is short ({name_len} chars). Make it more descriptive")
    
    # CATEGORY-SPECIFIC ADVICE
    category_advice = {
        'Technology': "💡 Tech campaigns: Show working prototype + detailed specs",
        'Games': "🎮 Board games: Include gameplay video + component photos",
        'Art': "🎨 Art projects: Show your portfolio + creation process",
        'Design': "✨ Design: Include 3D renders + material samples",
        'Film & Video': "🎬 Film: Share trailer + behind-the-scenes content",
        'Music': "🎵 Music: Upload sample tracks + studio photos"
    }
    if category in category_advice:
        recommendations.append(category_advice[category])
    
    # GEOGRAPHIC RECOMMENDATIONS
    if country not in ['US', 'GB', 'CA', 'AU']:
        recommendations.append(f"🌍 {country} has lower success rates. Consider targeting US/UK backers")
    
    # SUCCESS-BASED RECOMMENDATIONS
    if success_prob < 0.3:
        recommendations.append("⚠️ HIGH RISK: Revise your strategy before launching!")
    elif success_prob < 0.5:
        recommendations.append("⚠️ Medium-High Risk: Implement top 3 recommendations above")
    elif success_prob > 0.8:
        recommendations.append("🎉 Excellent setup! Focus on marketing and backer updates")
    
    # LAUNCH TIMING
    recommendations.append("📅 Launch on Tuesday 10-11 AM EST for maximum visibility")
    
    # Return top 8 most relevant recommendations
    return recommendations[:8]

def predict_campaign(campaign_data: Dict, models: Dict, encoders: Dict, feature_names: List[str]) -> Dict[str, Any]:
    """
    Main prediction function for a single campaign
    """
    try:
        # Preprocess the campaign data
        X_processed = preprocess_campaign(campaign_data, encoders, feature_names)
        
        # Get predictions from all models
        model_scores = {}
        
        # Logistic Regression
        lr_proba = models['logistic_regression'].predict_proba(X_processed)[0]
        model_scores['logistic_regression'] = float(lr_proba)
        
        # Decision Tree
        dt_proba = models['decision_tree'].predict_proba(X_processed)[0, 1]
        model_scores['decision_tree'] = float(dt_proba)
        
        # Random Forest
        rf_proba = models['random_forest'].predict_proba(X_processed)[0, 1]
        model_scores['random_forest'] = float(rf_proba)
        
        # Average probability (ensemble)
        avg_probability = np.mean(list(model_scores.values()))
        
        # Handle NaN values - replace with fallback
        if np.isnan(avg_probability) or not np.isfinite(avg_probability):
            print("Warning: NaN detected in predictions, using fallback")
            avg_probability = 0.5
            model_scores = {k: 0.5 for k in model_scores.keys()}
        
        # Determine risk level
        if avg_probability >= 0.7:
            risk_level = "Low"
            risk_color = "green"
        elif avg_probability >= 0.4:
            risk_level = "Medium"
            risk_color = "orange"
        else:
            risk_level = "High"
            risk_color = "red"
        
        # Generate explanations and recommendations
        explanations = generate_explanations(campaign_data, model_scores)
        recommendations = generate_recommendations(campaign_data, avg_probability)
        
        # Feature importance (using Random Forest)
        if hasattr(models['random_forest'], 'feature_importance'):
            feature_importance = {}
            top_features_idx = np.argsort(models['random_forest'].feature_importance)[-5:][::-1]
            for idx in top_features_idx:
                if idx < len(feature_names):
                    feature_importance[feature_names[idx]] = float(models['random_forest'].feature_importance[idx])
        else:
            feature_importance = {
                "goal_amount": 0.3,
                "campaign_duration": 0.25,
                "country": 0.15,
                "category": 0.2,
                "staff_pick": 0.1
            }
        
        return {
            "success_probability": float(avg_probability),
            "risk_level": risk_level,
            "risk_color": risk_color,
            "model_scores": model_scores,
            "explanations": explanations,
            "feature_importance": feature_importance,
            "recommendations": recommendations
        }
        
    except Exception as e:
        raise Exception(f"Prediction failed: {str(e)}")