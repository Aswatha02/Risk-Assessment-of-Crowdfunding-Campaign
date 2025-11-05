import numpy as np
from decision_tree import DecisionTree

class RandomForest:
    def __init__(self, n_trees=10, max_depth=10, min_samples_split=2, max_features=None):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.max_features = max_features
        self.trees = []
        self.feature_importance = None
        
    def _bootstrap_sample(self, X, y):
        n_samples = X.shape[0]
        indices = np.random.choice(n_samples, n_samples, replace=True)
        return X[indices], y[indices]
    
    def _get_random_features(self, n_features):
        if self.max_features is None:
            self.max_features = int(np.sqrt(n_features))
        
        return np.random.choice(n_features, self.max_features, replace=False)
    
    def fit(self, X, y):
        self.trees = []
        n_samples, n_features = X.shape
        
        # Initialize feature importance
        self.feature_importance = np.zeros(n_features)
        
        for i in range(self.n_trees):
            # Create bootstrap sample
            X_sample, y_sample = self._bootstrap_sample(X, y)
            
            # Get random feature subset
            feature_indices = self._get_random_features(n_features)
            X_sample_subset = X_sample[:, feature_indices]
            
            # Train decision tree on bootstrap sample with feature subset
            tree = DecisionTree(
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_split
            )
            tree.fit(X_sample_subset, y_sample)
            
            # Store tree and its feature mapping
            self.trees.append({
                'tree': tree,
                'feature_indices': feature_indices
            })
            
            # Aggregate feature importance
            for j, orig_idx in enumerate(feature_indices):
                if j < len(tree.feature_importance):
                    self.feature_importance[orig_idx] += tree.feature_importance[j]
        
        # Normalize feature importance
        self.feature_importance /= self.n_trees
    
    def predict(self, X):
        tree_preds = []
        for tree_data in self.trees:
            tree = tree_data['tree']
            feature_indices = tree_data['feature_indices']
            X_subset = X[:, feature_indices]
            pred = tree.predict(X_subset)
            tree_preds.append(pred)
        
        # Majority voting
        tree_preds = np.array(tree_preds)
        return np.round(np.mean(tree_preds, axis=0)).astype(int)
    
    def predict_proba(self, X):
        tree_preds = []
        for tree_data in self.trees:
            tree = tree_data['tree']
            feature_indices = tree_data['feature_indices']
            X_subset = X[:, feature_indices]
            pred = tree.predict(X_subset)
            tree_preds.append(pred)
        
        # Average probabilities
        tree_preds = np.array(tree_preds)
        proba = np.mean(tree_preds, axis=0)
        return np.column_stack([1 - proba, proba])