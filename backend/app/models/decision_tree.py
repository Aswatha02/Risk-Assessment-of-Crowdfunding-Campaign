import numpy as np

class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value
        
    def is_leaf(self):
        return self.value is not None

class DecisionTree:
    def __init__(self, max_depth=10, min_samples_split=2, min_impurity_decrease=0.0):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_impurity_decrease = min_impurity_decrease
        self.root = None
        self.feature_importance = None
        
    def _gini(self, y):
        """Calculate Gini impurity"""
        if len(y) == 0:
            return 0
        p1 = np.sum(y) / len(y)
        return 2 * p1 * (1 - p1)
    
    def _entropy(self, y):
        """Calculate entropy"""
        if len(y) == 0:
            return 0
        p1 = np.sum(y) / len(y)
        if p1 == 0 or p1 == 1:
            return 0
        return -p1 * np.log2(p1) - (1 - p1) * np.log2(1 - p1)
    
    def _information_gain(self, parent, left_child, right_child, criterion='gini'):
        """Calculate information gain"""
        if criterion == 'gini':
            metric = self._gini
        else:
            metric = self._entropy
            
        weight_left = len(left_child) / len(parent)
        weight_right = len(right_child) / len(parent)
        
        gain = metric(parent) - (weight_left * metric(left_child) + weight_right * metric(right_child))
        return gain
    
    def _best_split(self, X, y, criterion='gini'):
        best_gain = -1
        best_feature, best_threshold = None, None
        
        n_samples, n_features = X.shape
        
        for feature in range(n_features):
            # Consider unique thresholds
            thresholds = np.unique(X[:, feature])
            
            for threshold in thresholds:
                # Split data
                left_indices = X[:, feature] <= threshold
                right_indices = X[:, feature] > threshold
                
                if np.sum(left_indices) == 0 or np.sum(right_indices) == 0:
                    continue
                    
                # Calculate information gain
                gain = self._information_gain(
                    y, y[left_indices], y[right_indices], criterion
                )
                
                if gain > best_gain and gain >= self.min_impurity_decrease:
                    best_gain = gain
                    best_feature = feature
                    best_threshold = threshold
                    
        return best_feature, best_threshold, best_gain
    
    def _build_tree(self, X, y, depth=0):
        n_samples, n_features = X.shape
        
        # Stopping conditions
        if (depth >= self.max_depth or 
            n_samples < self.min_samples_split or 
            len(np.unique(y)) == 1):
            leaf_value = np.round(np.mean(y))  # Majority class
            return Node(value=leaf_value)
        
        # Find best split
        feature, threshold, gain = self._best_split(X, y)
        
        if feature is None:  # No split improves impurity
            leaf_value = np.round(np.mean(y))
            return Node(value=leaf_value)
        
        # Split data
        left_indices = X[:, feature] <= threshold
        right_indices = X[:, feature] > threshold
        
        # Recursively build left and right subtrees
        left = self._build_tree(X[left_indices], y[left_indices], depth + 1)
        right = self._build_tree(X[right_indices], y[right_indices], depth + 1)
        
        return Node(feature, threshold, left, right)
    
    def fit(self, X, y):
        self.root = self._build_tree(X, y)
        self._compute_feature_importance(X, y)
    
    def _compute_feature_importance(self, X, y):
        """Compute feature importance based on Gini importance"""
        n_features = X.shape[1]
        self.feature_importance = np.zeros(n_features)
        self._compute_importance_recursive(self.root, X, y)
        
        # Normalize
        if np.sum(self.feature_importance) > 0:
            self.feature_importance /= np.sum(self.feature_importance)
    
    def _compute_importance_recursive(self, node, X, y):
        if node.is_leaf():
            return
            
        # Calculate node impurity
        node_indices = np.ones(len(y), dtype=bool)  # This would need proper tracking
        node_impurity = self._gini(y)
        
        # Calculate importance for this split
        left_indices = X[:, node.feature] <= node.threshold
        right_indices = X[:, node.feature] > node.threshold
        
        n_node = len(y)
        n_left = np.sum(left_indices)
        n_right = np.sum(right_indices)
        
        # Weighted impurity decrease
        impurity_decrease = node_impurity - (
            (n_left / n_node) * self._gini(y[left_indices]) + 
            (n_right / n_node) * self._gini(y[right_indices])
        )
        
        self.feature_importance[node.feature] += impurity_decrease
        
        # Recurse
        self._compute_importance_recursive(node.left, X[left_indices], y[left_indices])
        self._compute_importance_recursive(node.right, X[right_indices], y[right_indices])
    
    def _predict_sample(self, x, node):
        if node.is_leaf():
            return node.value
            
        if x[node.feature] <= node.threshold:
            return self._predict_sample(x, node.left)
        else:
            return self._predict_sample(x, node.right)
    
    def predict(self, X):
        return np.array([self._predict_sample(x, self.root) for x in X])
    
    def predict_proba(self, X):
    # For binary classification, return probability based on leaf node value
        predictions = self.predict(X)
        # Return 2D array: [prob_class_0, prob_class_1]
        return np.column_stack([1 - predictions, predictions])