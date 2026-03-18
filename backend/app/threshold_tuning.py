"""
Threshold Tuning for Imbalanced Classification

This script finds the optimal classification threshold for each model
to maximize F1-score on the validation set.
"""

import numpy as np
import joblib
from preprocessing import run_preprocessing
from evaluation import ModelEvaluator

def find_optimal_threshold(y_true, y_pred_proba, metric='f1'):
    """
    Find optimal classification threshold to maximize given metric.
    
    Args:
        y_true: True labels
        y_pred_proba: Predicted probabilities
        metric: 'f1', 'precision', or 'recall'
    
    Returns:
        best_threshold: Optimal threshold value
        best_score: Best metric score
    """
    evaluator = ModelEvaluator()
    thresholds = np.arange(0.1, 0.9, 0.01)
    
    best_threshold = 0.5
    best_score = 0
    
    scores = []
    for threshold in thresholds:
        # Apply threshold
        y_pred = (y_pred_proba >= threshold).astype(int)
        
        # Calculate metric
        if metric == 'f1':
            score = evaluator.f1_score(y_true, y_pred)
        elif metric == 'precision':
            score = evaluator.precision_score(y_true, y_pred)
        elif metric == 'recall':
            score = evaluator.recall_score(y_true, y_pred)
        else:
            score = evaluator.accuracy_score(y_true, y_pred)
        
        scores.append(score)
        
        if score > best_score:
            best_score = score
            best_threshold = threshold
    
    return best_threshold, best_score, thresholds, scores

def tune_all_models():
    """Tune thresholds for all models on validation set."""
    
    print("Loading data...")
    X_train, X_val, X_test, y_train, y_val, y_test, encoders = run_preprocessing()
    
    # Convert to numpy
    numeric_cols = X_train.select_dtypes(include=[np.number]).columns
    X_val_np = X_val[numeric_cols].values
    y_val_np = y_val.values
    
    print("\nLoading trained models...")
    models_path = '../../trained_models/crowdrisk_models.pkl'
    model_package = joblib.load(models_path)
    
    lr_model = model_package['lr_model']
    dt_model = model_package['dt_model']
    rf_model = model_package['rf_model']
    
    models = {
        'Logistic Regression': lr_model,
        'Decision Tree': dt_model,
        'Random Forest': rf_model
    }
    
    optimal_thresholds = {}
    
    print("\n" + "="*60)
    print("THRESHOLD TUNING ON VALIDATION SET")
    print("="*60)
    
    for name, model in models.items():
        print(f"\n{name}:")
        print("-" * 40)
        
        # Get probabilities
        if hasattr(model, 'predict_proba'):
            proba_result = model.predict_proba(X_val_np)
            
            # Handle different probability formats
            if len(proba_result.shape) == 2 and proba_result.shape[1] == 2:
                y_pred_proba = proba_result[:, 1]
            else:
                y_pred_proba = proba_result
        else:
            print("  Model doesn't support predict_proba, skipping...")
            continue
        
        # Find optimal threshold
        best_threshold, best_f1, thresholds, scores = find_optimal_threshold(
            y_val_np, y_pred_proba, metric='f1'
        )
        
        optimal_thresholds[name] = best_threshold
        
        # Evaluate with default threshold (0.5)
        y_pred_default = (y_pred_proba >= 0.5).astype(int)
        evaluator = ModelEvaluator()
        
        print(f"  Default Threshold (0.5):")
        print(f"    Precision: {evaluator.precision_score(y_val_np, y_pred_default):.4f}")
        print(f"    Recall:    {evaluator.recall_score(y_val_np, y_pred_default):.4f}")
        print(f"    F1-Score:  {evaluator.f1_score(y_val_np, y_pred_default):.4f}")
        
        # Evaluate with optimal threshold
        y_pred_optimal = (y_pred_proba >= best_threshold).astype(int)
        
        print(f"\n  Optimal Threshold ({best_threshold:.2f}):")
        print(f"    Precision: {evaluator.precision_score(y_val_np, y_pred_optimal):.4f}")
        print(f"    Recall:    {evaluator.recall_score(y_val_np, y_pred_optimal):.4f}")
        print(f"    F1-Score:  {evaluator.f1_score(y_val_np, y_pred_optimal):.4f}")
        
        # Show confusion matrices
        cm_default = evaluator.confusion_matrix(y_val_np, y_pred_default)
        cm_optimal = evaluator.confusion_matrix(y_val_np, y_pred_optimal)
        
        print(f"\n  Confusion Matrix (Default):")
        print(f"    [[{cm_default[0,0]:>4} {cm_default[0,1]:>4}]")
        print(f"     [{cm_default[1,0]:>4} {cm_default[1,1]:>4}]]")
        
        print(f"\n  Confusion Matrix (Optimal):")
        print(f"    [[{cm_optimal[0,0]:>4} {cm_optimal[0,1]:>4}]")
        print(f"     [{cm_optimal[1,0]:>4} {cm_optimal[1,1]:>4}]]")
        
        improvement = (evaluator.f1_score(y_val_np, y_pred_optimal) - 
                      evaluator.f1_score(y_val_np, y_pred_default))
        print(f"\n  F1-Score Improvement: +{improvement:.4f}")
    
    print("\n" + "="*60)
    print("SUMMARY: OPTIMAL THRESHOLDS")
    print("="*60)
    for name, threshold in optimal_thresholds.items():
        print(f"  {name}: {threshold:.2f}")
    
    # Save optimal thresholds
    model_package['optimal_thresholds'] = optimal_thresholds
    joblib.dump(model_package, models_path)
    print(f"\nOptimal thresholds saved to {models_path}")

if __name__ == "__main__":
    tune_all_models()
