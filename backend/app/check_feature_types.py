import pandas as pd
import numpy as np

# Load processed dataset
df = pd.read_csv('../../data/processed/processed.csv', low_memory=False)

print("="*60)
print("FEATURE TYPE ANALYSIS")
print("="*60)
print(f"Total features: {df.shape[1]}")
print(f"Total rows: {df.shape[0]}")

# Separate by data type
numeric_features = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_features = df.select_dtypes(include=['object']).columns.tolist()

# Remove target variable from counts
if 'SuccessfulBool' in numeric_features:
    numeric_features.remove('SuccessfulBool')

print(f"\n{'='*60}")
print(f"NUMERICAL FEATURES: {len(numeric_features)}")
print("="*60)
for i, feat in enumerate(numeric_features, 1):
    dtype = df[feat].dtype
    print(f"{i:2d}. {feat:40s} ({dtype})")

print(f"\n{'='*60}")
print(f"CATEGORICAL FEATURES: {len(categorical_features)}")
print("="*60)
for i, feat in enumerate(categorical_features, 1):
    unique_count = df[feat].nunique()
    print(f"{i:2d}. {feat:40s} ({unique_count} unique values)")

print(f"\n{'='*60}")
print("SUMMARY")
print("="*60)
print(f"Numerical features:   {len(numeric_features)}")
print(f"Categorical features: {len(categorical_features)}")
print(f"Target variable:      1 (SuccessfulBool)")
print(f"Total:                {len(numeric_features) + len(categorical_features) + 1}")

# Check which categorical features are encoded
print(f"\n{'='*60}")
print("CATEGORICAL FEATURES BREAKDOWN")
print("="*60)

datetime_features = []
text_features = []
encoded_features = []
raw_categorical = []

for feat in categorical_features:
    if feat in ['deadline', 'created_at', 'launched_at']:
        datetime_features.append(feat)
    elif feat in ['name', 'blurb', 'name_clean', 'blurb_clean']:
        text_features.append(feat)
    elif feat.endswith('_te'):
        encoded_features.append(feat)
    else:
        raw_categorical.append(feat)

print(f"\nDatetime features: {len(datetime_features)}")
for feat in datetime_features:
    print(f"  - {feat}")

print(f"\nText features: {len(text_features)}")
for feat in text_features:
    print(f"  - {feat}")

print(f"\nTarget-encoded features: {len(encoded_features)}")
for feat in encoded_features:
    print(f"  - {feat}")

print(f"\nRaw categorical features: {len(raw_categorical)}")
for feat in raw_categorical:
    unique_count = df[feat].nunique()
    print(f"  - {feat} ({unique_count} unique values)")

print(f"\n{'='*60}")
print("FEATURES USED FOR MODELING (After Encoding)")
print("="*60)
print(f"Numerical features:        {len(numeric_features)}")
print(f"Target-encoded features:   {len(encoded_features)} (categorical -> numerical)")
print(f"Total modeling features:   {len(numeric_features) + len(encoded_features)}")
print(f"\nExcluded from modeling:")
print(f"  - Datetime: {len(datetime_features)} (used for feature extraction)")
print(f"  - Text: {len(text_features)} (used for text analysis)")
print(f"  - Raw categorical: {len(raw_categorical)} (replaced by target encoding)")
