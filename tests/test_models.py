import sys
import os
import numpy as np

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend', 'app'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend', 'app', 'models'))

from logistic_regression import LogisticRegression
from decision_tree import DecisionTree
from random_forest import RandomForest

def test_logistic_regression():
    print("🧪 Testing Logistic Regression...")
    
    # Create simple linearly separable data
    np.random.seed(42)
    X = np.random.randn(100, 3)
    y = (X[:, 0] + 2*X[:, 1] - X[:, 2] > 0).astype(int)
    
    model = LogisticRegression(learning_rate=0.1, n_iters=500)
    model.fit(X, y)
    
    predictions = model.predict(X)
    accuracy = np.mean(predictions == y)
    
    print(f"   Accuracy: {accuracy:.4f}")
    assert accuracy > 0.85, "Logistic Regression should achieve >85% accuracy on simple data"
    print("   ✅ Logistic Regression test passed!")

def test_decision_tree():
    print("🧪 Testing Decision Tree...")
    
    # Create XOR-like data (non-linearly separable)
    np.random.seed(42)
    X = np.random.randn(200, 2)
    y = ((X[:, 0] > 0) ^ (X[:, 1] > 0)).astype(int)
    
    model = DecisionTree(max_depth=5)
    model.fit(X, y)
    
    predictions = model.predict(X)
    accuracy = np.mean(predictions == y)
    
    print(f"   Accuracy: {accuracy:.4f}")
    assert accuracy > 0.80, "Decision Tree should handle non-linear data"
    print("   ✅ Decision Tree test passed!")

def test_random_forest():
    print("🧪 Testing Random Forest...")
    
    # Create complex data
    np.random.seed(42)
    X = np.random.randn(300, 4)
    y = (X[:, 0]**2 + X[:, 1]**2 > 1).astype(int)
    
    model = RandomForest(n_trees=10, max_depth=5)
    model.fit(X, y)
    
    predictions = model.predict(X)
    accuracy = np.mean(predictions == y)
    
    print(f"   Accuracy: {accuracy:.4f}")
    assert accuracy > 0.85, "Random Forest should perform well on complex data"
    print("   ✅ Random Forest test passed!")

def test_all_models():
    print("🚀 Starting Comprehensive Model Tests...")
    print("=" * 50)
    
    test_logistic_regression()
    test_decision_tree() 
    test_random_forest()
    
    print("=" * 50)
    print("🎉 All model tests passed successfully!")
    print("   All ML models implemented from scratch are working correctly!")

if __name__ == "__main__":
    test_all_models()