# backend/app/train.py
import pandas as pd
import joblib
from pathlib import Path

# Import our from-scratch components
from preprocessing import full_preprocessing_pipeline
#from models.logistic_regression import LogisticRegression
#from models.decision_tree import DecisionTree
#from evaluation import evaluate_model

def train_crowdrisk():
    print("🚀 Starting CrowdRisk Training Pipeline")
    print("=" * 50)
    
    # 1. Preprocessing
    print("\n📊 Step 1: Preprocessing Data...")
    data_path = '../../data/raw/kickstarter_data_full.csv'
    
    try:
        # ✅ Adjusted unpacking to match the fixed preprocessing.py
        X_train, X_val, X_test, y_train, y_val, y_test, target_encoders = full_preprocessing_pipeline(
            data_path, is_training=True
        )
        
        print(f"✅ Preprocessing complete!")
        print(f"   Training set: {X_train.shape}")
        print(f"   Validation set: {X_val.shape}")
        print(f"   Test set: {X_test.shape}")
        
    except FileNotFoundError:
        print(f"❌ Error: Data file not found at {data_path}")
        return
    except Exception as e:
        print(f"❌ Error during preprocessing: {e}")
        return

    # 2. Train Models
    print("\n🤖 Step 2: Training Models...")
    
    # Logistic Regression
    print("   Training Logistic Regression...")
    lr_model = LogisticRegression(learning_rate=0.01, n_iters=1000)
    lr_model.fit(X_train, y_train)
    
    # Decision Tree
    print("   Training Decision Tree...")
    dt_model = DecisionTree(max_depth=5)
    dt_model.fit(X_train, y_train)
    
    print("✅ Model training complete!")

    # 3. Evaluate Models
    print("\n📈 Step 3: Evaluating Models...")
    
    print("   Logistic Regression Performance:")
    lr_val_pred = lr_model.predict(X_val)
    evaluate_model(y_val, lr_val_pred, "Validation Set")
    
    print("\n   Decision Tree Performance:")
    dt_val_pred = dt_model.predict(X_val)
    evaluate_model(y_val, dt_val_pred, "Validation Set")
    
    # 4. Save Everything
    print("\n💾 Step 4: Saving Models and Artifacts...")
    
    models_dir = Path('../../trained_models')
    models_dir.mkdir(exist_ok=True)
    
    model_package = {
        'lr_model': lr_model,
        'dt_model': dt_model,
        'target_encoders': target_encoders,
        'feature_names': getattr(X_train, 'columns', None),
        'model_metadata': {
            'training_date': pd.Timestamp.now(),
            'dataset_shape': f"{X_train.shape[0]} samples, {X_train.shape[1]} features",
            'class_distribution': f"Success: {y_train.mean():.2%}, Fail: {1 - y_train.mean():.2%}"
        }
    }
    
    joblib.dump(model_package, models_dir / 'crowdrisk_models.pkl')
    print(f"✅ Models saved to {models_dir / 'crowdrisk_models.pkl'}")

    # 5. Final Test Evaluation
    print("\n🎯 Step 5: Final Test Evaluation (Unseen Data)...")
    
    print("   Logistic Regression - Test Set:")
    lr_test_pred = lr_model.predict(X_test)
    evaluate_model(y_test, lr_test_pred, "Test Set")
    
    print("\n   Decision Tree - Test Set:")
    dt_test_pred = dt_model.predict(X_test)
    evaluate_model(y_test, dt_test_pred, "Test Set")
    
    print("\n" + "=" * 50)
    print("🎉 CrowdRisk Training Pipeline Completed Successfully!")
    
    return lr_model, dt_model, target_encoders

if __name__ == "__main__":
    train_crowdrisk()
