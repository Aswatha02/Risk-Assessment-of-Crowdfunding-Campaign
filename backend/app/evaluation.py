import numpy as np
import matplotlib.pyplot as plt

class ModelEvaluator:
    def __init__(self):
        self.metrics = {}
    
    def accuracy_score(self, y_true, y_pred):
        return np.mean(y_true == y_pred)
    
    def precision_score(self, y_true, y_pred):
        true_positives = np.sum((y_pred == 1) & (y_true == 1))
        predicted_positives = np.sum(y_pred == 1)
        return true_positives / predicted_positives if predicted_positives > 0 else 0
    
    def recall_score(self, y_true, y_pred):
        true_positives = np.sum((y_pred == 1) & (y_true == 1))
        actual_positives = np.sum(y_true == 1)
        return true_positives / actual_positives if actual_positives > 0 else 0
    
    def f1_score(self, y_true, y_pred):
        precision = self.precision_score(y_true, y_pred)
        recall = self.recall_score(y_true, y_pred)
        if precision + recall == 0:
            return 0
        return 2 * (precision * recall) / (precision + recall)
    
    def confusion_matrix(self, y_true, y_pred):
        tp = np.sum((y_pred == 1) & (y_true == 1))
        fp = np.sum((y_pred == 1) & (y_true == 0))
        tn = np.sum((y_pred == 0) & (y_true == 0))
        fn = np.sum((y_pred == 0) & (y_true == 1))
        return np.array([[tn, fp], [fn, tp]])
    
    def roc_curve(self, y_true, y_pred_proba):
        thresholds = np.linspace(0, 1, 100)
        tpr = []  # True Positive Rate
        fpr = []  # False Positive Rate
        
        for threshold in thresholds:
            y_pred = (y_pred_proba >= threshold).astype(int)
            cm = self.confusion_matrix(y_true, y_pred)
            tn, fp, fn, tp = cm[0, 0], cm[0, 1], cm[1, 0], cm[1, 1]
            
            tpr_val = tp / (tp + fn) if (tp + fn) > 0 else 0
            fpr_val = fp / (fp + tn) if (fp + tn) > 0 else 0
            
            tpr.append(tpr_val)
            fpr.append(fpr_val)
        
        return fpr, tpr, thresholds
    
    def auc_score(self, fpr, tpr):
        # Calculate Area Under Curve using trapezoidal rule
        auc = 0
        for i in range(1, len(fpr)):
            auc += (fpr[i] - fpr[i-1]) * (tpr[i] + tpr[i-1]) / 2
        return auc
    
    def evaluate_model(self, y_true, y_pred, y_pred_proba=None, model_name="Model"):
        metrics = {}
        
        metrics['accuracy'] = self.accuracy_score(y_true, y_pred)
        metrics['precision'] = self.precision_score(y_true, y_pred)
        metrics['recall'] = self.recall_score(y_true, y_pred)
        metrics['f1'] = self.f1_score(y_true, y_pred)
        metrics['confusion_matrix'] = self.confusion_matrix(y_true, y_pred)
        
        if y_pred_proba is not None:
            # Handle both 1D and 2D probability arrays
            if len(y_pred_proba.shape) == 2 and y_pred_proba.shape[1] == 2:
                y_pred_proba_1d = y_pred_proba[:, 1]  # Get probabilities for class 1
            else:
                y_pred_proba_1d = y_pred_proba  # Already 1D
            
            fpr, tpr, thresholds = self.roc_curve(y_true, y_pred_proba_1d)
            metrics['auc'] = self.auc_score(fpr, tpr)
            metrics['roc_curve'] = {'fpr': fpr, 'tpr': tpr}
        
        self.metrics[model_name] = metrics
        return metrics
    
    def print_metrics(self, metrics, model_name="Model"):
        print(f"\n{model_name} Evaluation:")
        print(f"   Accuracy:  {metrics['accuracy']:.4f}")
        print(f"   Precision: {metrics['precision']:.4f}")
        print(f"   Recall:    {metrics['recall']:.4f}")
        print(f"   F1-Score:  {metrics['f1']:.4f}")
        if 'auc' in metrics:
            print(f"   AUC:       {metrics['auc']:.4f}")
        
        cm = metrics['confusion_matrix']
        print(f"   Confusion Matrix:")
        print(f"   [[{cm[0,0]:>4} {cm[0,1]:>4}]")
        print(f"    [{cm[1,0]:>4} {cm[1,1]:>4}]]")

def evaluate_all_models(models, X_test, y_test, model_names):
    evaluator = ModelEvaluator()
    results = {}
    
    for i, (model, name) in enumerate(zip(models, model_names)):
        print(f"\nEvaluating {name}...")
        
        # Get predictions
        y_pred = model.predict(X_test)
        
        # Get probabilities (handle different model types)
        y_pred_proba = None
        if hasattr(model, 'predict_proba'):
            try:
                proba_result = model.predict_proba(X_test)
                # Handle different probability array shapes
                if len(proba_result.shape) == 2 and proba_result.shape[1] == 2:
                    y_pred_proba = proba_result[:, 1]  # Binary classification, get class 1 probabilities
                else:
                    y_pred_proba = proba_result  # Use as is
            except Exception as e:
                print(f"   Warning: Could not get probabilities: {e}")
                y_pred_proba = None
        
        metrics = evaluator.evaluate_model(y_test, y_pred, y_pred_proba, name)
        evaluator.print_metrics(metrics, name)
        results[name] = metrics
    
    return results, evaluator