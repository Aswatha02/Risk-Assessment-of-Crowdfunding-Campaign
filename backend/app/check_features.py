import pandas as pd

# Check raw dataset
print("="*60)
print("RAW DATASET")
print("="*60)
df_raw = pd.read_csv('../../data/raw/kickstarter_data_full.csv', low_memory=False)
print(f"Total columns: {df_raw.shape[1]}")
print(f"Total rows: {df_raw.shape[0]}")
print(f"\nColumn names:")
for i, col in enumerate(df_raw.columns, 1):
    print(f"{i:2d}. {col}")

# Check processed dataset
print("\n" + "="*60)
print("PROCESSED DATASET (After Feature Engineering)")
print("="*60)
df_processed = pd.read_csv('../../data/processed/processed.csv', low_memory=False)
print(f"Total columns: {df_processed.shape[1]}")
print(f"Total rows: {df_processed.shape[0]}")
print(f"\nColumn names:")
for i, col in enumerate(df_processed.columns, 1):
    print(f"{i:2d}. {col}")

# Find engineered features (in processed but not in raw)
raw_cols = set(df_raw.columns)
processed_cols = set(df_processed.columns)

engineered = processed_cols - raw_cols
removed = raw_cols - processed_cols

print("\n" + "="*60)
print("FEATURE ENGINEERING SUMMARY")
print("="*60)
print(f"Original features: {len(raw_cols)}")
print(f"Features after engineering: {len(processed_cols)}")
print(f"Engineered features (NEW): {len(engineered)}")
print(f"Removed features: {len(removed)}")

print(f"\n{'='*60}")
print(f"ENGINEERED FEATURES ({len(engineered)} total):")
print("="*60)
for i, feat in enumerate(sorted(engineered), 1):
    print(f"{i:2d}. {feat}")

print(f"\n{'='*60}")
print(f"REMOVED FEATURES ({len(removed)} total):")
print("="*60)
for i, feat in enumerate(sorted(removed), 1):
    print(f"{i:2d}. {feat}")
