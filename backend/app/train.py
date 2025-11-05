import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path
import joblib

# Add the models directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

from preprocessing import run_preprocessing
from logistic_regression import LogisticRegression
from decision_tree import DecisionTree
from random_forest import RandomForest
from evaluation import evaluate_all_models

def train_crowdrisk():
    print("🚀 Starting CrowdRisk Training Pipeline")
    print("=" * 50)
    
    # 1. Preprocessing
    print("\n📊 Step 1: Preprocessing Data...")
    
    try:
        X_train, X_val, X_test, y_train, y_val, y_test, encoders = run_preprocessing()
        
        print(f"✅ Preprocessing complete!")
        print(f"   Training set: {X_train.shape}")
        print(f"   Validation set: {X_val.shape}")
        print(f"   Test set: {X_test.shape}")
        
    except Exception as e:
        print(f"❌ Error during preprocessing: {e}")
        import traceback
        traceback.print_exc()
        return

    # Convert to numpy arrays for our models (keep only numeric columns)
    numeric_cols = X_train.select_dtypes(include=[np.number]).columns
    X_train_np = X_train[numeric_cols].values
    X_val_np = X_val[numeric_cols].values  
    X_test_np = X_test[numeric_cols].values
    y_train_np = y_train.values
    y_val_np = y_val.values
    y_test_np = y_test.values

    print(f"\n📈 Data Overview:")
    print(f"   Training samples: {X_train_np.shape[0]}")
    print(f"   Features: {X_train_np.shape[1]}")
    print(f"   Success rate: {y_train_np.mean():.2%}")

    # 2. Train Models
    print("\n🤖 Step 2: Training Models...")
    
    models = []
    model_names = []
    
    # Logistic Regression
    print("   📈 Training Logistic Regression...")
    lr_model = LogisticRegression(learning_rate=0.01, n_iters=2000)
    lr_model.fit(X_train_np, y_train_np)
    models.append(lr_model)
    model_names.append("Logistic Regression")
    
    # Decision Tree
    print("   🌳 Training Decision Tree...")
    dt_model = DecisionTree(max_depth=8, min_samples_split=20)
    dt_model.fit(X_train_np, y_train_np)
    models.append(dt_model)
    model_names.append("Decision Tree")
    
    # Random Forest
    print("   🌲 Training Random Forest...")
    rf_model = RandomForest(n_trees=20, max_depth=8, min_samples_split=20)
    rf_model.fit(X_train_np, y_train_np)
    models.append(rf_model)
    model_names.append("Random Forest")
    
    print("✅ Model training complete!")

    # 3. Evaluate Models
    print("\n📊 Step 3: Evaluating Models...")
    
    print("\n🔍 Validation Set Performance:")
    results_val, evaluator_val = evaluate_all_models(models, X_val_np, y_val_np, model_names)
    
    print("\n🎯 Test Set Performance:")
    results_test, evaluator_test = evaluate_all_models(models, X_test_np, y_test_np, model_names)

    # 4. Save Models and Artifacts
    print("\n💾 Step 4: Saving Models and Artifacts...")
    
    models_dir = Path('../../trained_models')
    models_dir.mkdir(exist_ok=True)
    
    # Prepare model package
    model_package = {
        'lr_model': lr_model,
        'dt_model': dt_model, 
        'rf_model': rf_model,
        'encoders': encoders,
        'feature_names': numeric_cols.tolist(),
        'preprocessing_info': {
            'numeric_columns': numeric_cols.tolist(),
            'target_column': 'SuccessfulBool'
        },
        'evaluation_results': {
            'validation': results_val,
            'test': results_test
        },
        'model_metadata': {
            'training_date': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            'dataset_shape': f"{X_train.shape[0]} samples, {X_train.shape[1]} features",
            'class_distribution': f"Success: {y_train.mean():.2%}, Fail: {1 - y_train.mean():.2%}",
            'models_trained': model_names
        }
    }
    
    # Save models
    joblib.dump(model_package, models_dir / 'crowdrisk_models.pkl')
    print(f"✅ Models saved to {models_dir / 'crowdrisk_models.pkl'}")
    
    # Save feature names separately for easy access
    with open(models_dir / 'feature_names.txt', 'w') as f:
        for i, name in enumerate(numeric_cols):
            f.write(f"{i}: {name}\n")
    
    # 5. Feature Importance Analysis
    print("\n🔍 Step 5: Feature Importance Analysis...")
    
    # Get feature importance from Random Forest (most reliable)
    if hasattr(rf_model, 'feature_importance'):
        feature_importance = rf_model.feature_importance
        top_features_idx = np.argsort(feature_importance)[-10:][::-1]  # Top 10 features
        
        print("\n🎯 Top 10 Most Important Features:")
        for i, idx in enumerate(top_features_idx):
            print(f"   {i+1:2d}. {numeric_cols[idx]}: {feature_importance[idx]:.4f}")
    
    print("\n" + "=" * 50)
    print("🎉 CrowdRisk Training Pipeline Completed Successfully!")
    print("   Next: Start the API server with 'uvicorn main:app --reload'")
    
    return models, model_names, encoders

if __name__ == "__main__":
    train_crowdrisk()