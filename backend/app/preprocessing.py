# backend/app/preprocessing.py
import os
import pandas as pd
import numpy as np
import ast
from datetime import datetime
import random
import re

# ---------------------------
# CONFIG
# ---------------------------
TARGET_COL = "SuccessfulBool"

# ---------------------------
# Utilities
# ---------------------------
def safe_literal_eval(x):
    """Try to literal_eval a JSON-like string, otherwise return None."""
    try:
        if pd.isna(x):
            return None
        if isinstance(x, dict):
            return x
        if isinstance(x, str) and (x.startswith("{") or x.startswith("[")):
            return ast.literal_eval(x)
        return None
    except Exception:
        return None

def parse_timedelta_string(td_str):
    """Parse timedelta strings like '17 days 14:51:39.000000000' into days"""
    try:
        if pd.isna(td_str) or td_str == "":
            return 0
        
        # Handle different formats
        if "days" in str(td_str):
            # Format: "17 days 14:51:39.000000000"
            parts = str(td_str).split()
            days = int(parts[0])
            
            if len(parts) > 2:
                time_parts = parts[2].split(':')
                hours = int(time_parts[0])
                minutes = int(time_parts[1])
                seconds = float(time_parts[2])
                fractional_day = (hours + minutes/60 + seconds/3600) / 24
                return days + fractional_day
            return days
        else:
            # Try to convert directly to numeric
            return float(td_str)
    except:
        return 0

# ---------------------------
# 1. Load data
# ---------------------------
def load_data(filepath):
    df = pd.read_csv(filepath, low_memory=False)
    print(f"Data loaded. Shape: {df.shape}")
    return df

# ---------------------------
# 2. Clean data
# ---------------------------
def clean_data(df):
    df_clean = df.copy()
    
    # Drop useless columns (including the ones you don't want)
    drop_cols = ["slug", "urls", "source_url", "friends", "permissions", "profile", "is_starred", "is_backing", "location"]
    df_clean.drop(columns=[c for c in drop_cols if c in df_clean.columns], inplace=True)
    
    # Fill text columns
    for c in ["name", "blurb", "country", "currency", "currency_symbol", "category"]:
        if c in df_clean.columns:
            df_clean[c] = df_clean[c].fillna("")
    
    # Fill numeric columns
    numeric_cols = ["goal", "pledged", "backers_count", "static_usd_rate", "usd_pledged"]
    for c in numeric_cols:
        if c in df_clean.columns:
            df_clean[c] = pd.to_numeric(df_clean[c], errors="coerce").fillna(0.0)
    
    # Map boolean-like columns
    bool_cols = ["disable_communication", "staff_pick", "spotlight"]
    for c in bool_cols:
        if c in df_clean.columns:
            df_clean[c] = df_clean[c].map(
                lambda v: 1 if str(v).strip().upper() in ("TRUE", "1", "T", "Y", "YES") else 0
            )
    
    # Parse datetime columns but keep them as datetime objects
    date_cols = [c for c in ["deadline", "state_changed_at", "created_at", "launched_at"] if c in df_clean.columns]
    for c in date_cols:
        def _to_dt(x):
            if pd.isna(x):
                return pd.NaT
            if isinstance(x, (int, float)) and not np.isnan(x):
                try:
                    if x > 1e12:
                        return pd.to_datetime(int(x), unit="ms", errors="coerce")
                    elif x > 1e9:
                        return pd.to_datetime(int(x), unit="s", errors="coerce")
                except Exception:
                    pass
            try:
                return pd.to_datetime(x, errors="coerce")
            except:
                return pd.NaT
        df_clean[c] = df_clean[c].apply(_to_dt)
    
    # Parse timedelta columns (create_to_launch, launch_to_deadline, launch_to_state_change)
    timedelta_cols = ["create_to_launch", "launch_to_deadline", "launch_to_state_change"]
    for c in timedelta_cols:
        if c in df_clean.columns:
            df_clean[c] = df_clean[c].apply(parse_timedelta_string)
    
    # Drop rows with missing essential dates
    if "launched_at" in df_clean.columns and "deadline" in df_clean.columns:
        before = df_clean.shape[0]
        df_clean = df_clean.dropna(subset=["launched_at", "deadline"])
        after = df_clean.shape[0]
        if before != after:
            print(f"Dropped {before-after} rows due to missing essential dates")
    
    # Create target column if not present
    if "state" in df_clean.columns and TARGET_COL not in df_clean.columns:
        df_clean[TARGET_COL] = (df_clean["state"].astype(str).str.lower() == "successful").astype(int)
    
    print(f"Data cleaned. New shape: {df_clean.shape}")
    return df_clean

# ---------------------------
# 3. Feature engineering
# ---------------------------
def engineer_features(df):
    df_feat = df.copy()
    
    # Currency features
    df_feat["goal_usd"] = df_feat["goal"] * df_feat.get("static_usd_rate", 1.0)
    if "usd_pledged" in df_feat.columns:
        df_feat["pledged_usd"] = pd.to_numeric(df_feat["usd_pledged"], errors="coerce").fillna(
            df_feat["pledged"] * df_feat.get("static_usd_rate", 1.0)
        )
    else:
        df_feat["pledged_usd"] = df_feat["pledged"] * df_feat.get("static_usd_rate", 1.0)
    
    # Duration features - keep as is (don't change create_to_launch_days, launch_to_deadline_days, launch_to_state_change_days)
    if "launched_at" in df_feat.columns and "deadline" in df_feat.columns and "created_at" in df_feat.columns and "state_changed_at" in df_feat.columns:
        # Only create these if they don't already exist
        if "launch_to_deadline_days" not in df_feat.columns:
            df_feat["launch_to_deadline_days"] = (df_feat["deadline"] - df_feat["launched_at"]).dt.days.fillna(0).astype(int)
        if "create_to_launch_days" not in df_feat.columns:
            df_feat["create_to_launch_days"] = (df_feat["launched_at"] - df_feat["created_at"]).dt.days.fillna(0).astype(int)
        if "launch_to_state_change_days" not in df_feat.columns:
            df_feat["launch_to_state_change_days"] = (df_feat["state_changed_at"] - df_feat["launched_at"]).dt.days.fillna(0).astype(int)
    else:
        if "launch_to_deadline_days" not in df_feat.columns:
            df_feat["launch_to_deadline_days"] = 0
        if "create_to_launch_days" not in df_feat.columns:
            df_feat["create_to_launch_days"] = 0
        if "launch_to_state_change_days" not in df_feat.columns:
            df_feat["launch_to_state_change_days"] = 0
    
    # Duration risk
    df_feat["duration_risk_short"] = (df_feat["launch_to_deadline_days"] < 7).astype(int)
    df_feat["duration_risk_long"] = (df_feat["launch_to_deadline_days"] > 90).astype(int)
    
    # Launch timing - create weekday features for all datetime columns
    datetime_cols = ["deadline", "state_changed_at", "created_at", "launched_at"]
    for col in datetime_cols:
        if col in df_feat.columns:
            weekday_col = f"{col}_weekday"
            if weekday_col not in df_feat.columns:  # Only create if it doesn't exist
                df_feat[weekday_col] = df_feat[col].dt.weekday.fillna(0).astype(int)
    
    if "launched_at" in df_feat.columns:
        df_feat["launch_hour"] = df_feat["launched_at"].dt.hour.fillna(0).astype(int)
        df_feat["launch_weekday"] = df_feat["launched_at"].dt.weekday.fillna(0).astype(int)
        df_feat["launch_month"] = df_feat["launched_at"].dt.month.fillna(0).astype(int)
        df_feat["launch_is_weekend"] = df_feat["launch_weekday"].isin([5,6]).astype(int)
        
        # Check if launched on Tuesday (your specific requirement)
        df_feat["launched_tuesday"] = (df_feat["launch_weekday"] == 1).astype(int)
    
    # Text features - keep name_len_clean and blurb_len_clean as is
    df_feat["name_clean"] = df_feat.get("name", "").astype(str).str.lower()
    df_feat["blurb_clean"] = df_feat.get("blurb", "").astype(str).str.lower()
    df_feat["name_len_clean"] = df_feat["name_clean"].str.len()
    df_feat["blurb_len_clean"] = df_feat["blurb_clean"].str.len()
    df_feat["blurb_exclaims"] = df_feat["blurb_clean"].str.count("!")
    
    # Sentiment analysis (simple word count approach)
    positive_words = ["amazing", "innovative", "exciting", "unique", "help", "support", "love", "new", "great", "wonderful"]
    negative_words = ["delay", "problem", "issue", "cancel", "refund", "risk", "challenge", "difficult"]
    
    df_feat["blurb_positive_score"] = df_feat["blurb_clean"].apply(
        lambda t: sum(t.count(w) for w in positive_words) if isinstance(t, str) else 0
    )
    df_feat["blurb_negative_score"] = df_feat["blurb_clean"].apply(
        lambda t: sum(t.count(w) for w in negative_words) if isinstance(t, str) else 0
    )
    df_feat["text_sentiment_score"] = df_feat["blurb_positive_score"] - df_feat["blurb_negative_score"]
    df_feat["text_quality_score"] = (df_feat["blurb_positive_score"] * 2 + df_feat["blurb_len_clean"]/100) - df_feat["blurb_negative_score"]
    
    # Creator features
    if "creator" in df_feat.columns:
        df_feat["creator_parsed"] = df_feat["creator"].apply(safe_literal_eval)
        df_feat["creator_has_avatar"] = df_feat["creator_parsed"].apply(
            lambda d: 1 if (isinstance(d, dict) and d.get("avatar") and d["avatar"].get("small")) else 0
        )
        df_feat["creator_id"] = df_feat["creator_parsed"].apply(
            lambda d: d.get("id") if isinstance(d, dict) else None
        )
        creator_counts = df_feat["creator_id"].value_counts().to_dict()
        df_feat["creator_project_count"] = df_feat["creator_id"].map(
            lambda cid: creator_counts.get(cid, 1)
        ).fillna(1).astype(int)
        df_feat["creator_reputation"] = np.log1p(df_feat["creator_project_count"])  # Log transform for better distribution
    else:
        df_feat["creator_has_avatar"] = 0
        df_feat["creator_project_count"] = 1
        df_feat["creator_reputation"] = 0
    
    # Photo features
    if "photo" in df_feat.columns:
        df_feat["photo_parsed"] = df_feat["photo"].apply(safe_literal_eval)
        df_feat["photo_count"] = df_feat["photo_parsed"].apply(
            lambda x: len(x) if isinstance(x, dict) else 0
        )
    else:
        df_feat["photo_count"] = 0
    
    # Category-specific benchmarks
    if "category" in df_feat.columns:
        # Calculate average goal by category
        category_avg_goal = df_feat.groupby("category")["goal_usd"].mean().to_dict()
        df_feat["category_avg_goal"] = df_feat["category"].map(category_avg_goal)
        df_feat["goal_vs_category_benchmark"] = df_feat["goal_usd"] / (df_feat["category_avg_goal"] + 1e-9)
    
    # Geographic hub score
    if "country" in df_feat.columns:
        # Calculate success rate by country
        country_success_rate = df_feat.groupby("country")[TARGET_COL].mean().to_dict()
        df_feat["country_success_rate"] = df_feat["country"].map(country_success_rate).fillna(0.5)
        
        # Identify if US or GB (your specific requirement) - don't change USorGB
        if "USorGB" not in df_feat.columns:
            df_feat["USorGB"] = df_feat["country"].isin(["US", "GB"]).astype(int)
        
        # Top countries (your specific requirement) - don't change TOPCOUNTRY
        if "TOPCOUNTRY" not in df_feat.columns:
            top_countries = df_feat["country"].value_counts().head(5).index.tolist()
            df_feat["TOPCOUNTRY"] = df_feat["country"].isin(top_countries).astype(int)
    
    # Interaction features
    df_feat["backers_count"] = pd.to_numeric(df_feat.get("backers_count", 0), errors="coerce").fillna(0).astype(int)
    df_feat["goal_per_backer"] = df_feat["goal_usd"] / (df_feat["backers_count"] + 1)
    df_feat["pledge_ratio"] = df_feat["pledged_usd"] / (df_feat["goal_usd"] + 1e-9)
    
    # Goal-Backer Elasticity
    df_feat["goal_backer_elasticity"] = np.log1p(df_feat["backers_count"]) / (np.log1p(df_feat["goal_usd"]) + 1e-9)
    
    # Check if deadline is on weekend (your specific requirement)
    if "deadline" in df_feat.columns:
        if "deadline_weekday" not in df_feat.columns:  # Only create if it doesn't exist
            df_feat["deadline_weekday"] = df_feat["deadline"].dt.weekday.fillna(0).astype(int)
        df_feat["DeadlineWeekend"] = df_feat["deadline_weekday"].isin([5, 6]).astype(int)
    
    print(f"Feature engineering complete. New shape: {df_feat.shape}")
    return df_feat

# ---------------------------
# 4. Encode categorical features
# ---------------------------
def manual_target_encode(series, target):
    encoding_map = {}
    ser = series.fillna("___missing___")
    for val in ser.unique():
        mask = (ser == val)
        encoding_map[val] = float(target[mask].mean()) if mask.sum() > 0 else float(target.mean())
    return ser.map(encoding_map), encoding_map

def encode_and_prepare(df, target_encoders=None, is_training=True):
    if target_encoders is None:
        target_encoders = {}
    else:
        target_encoders = target_encoders.copy()
    
    df_final = df.copy()
    
    # Keep datetime columns as they are (don't convert to Unix timestamp)
    categorical_cols = ["category", "country", "currency", "currency_symbol"]
    
    if is_training:
        for col in categorical_cols:
            if col in df_final.columns:
                enc_series, enc_map = manual_target_encode(df_final[col], df_final[TARGET_COL])
                df_final[f"{col}_te"] = enc_series
                target_encoders[col] = enc_map
    else:
        for col in categorical_cols:
            enc_map = target_encoders.get(col, {})
            df_final[f"{col}_te"] = df_final[col].fillna("___missing___").map(enc_map)
            df_final[f"{col}_te"] = df_final[f"{col}_te"].fillna(target_encoders.get("global_mean", 0.5))
    
    # Drop only the columns we need to drop, keeping name, blurb, and datetime columns
    drop_cols = ["creator", "creator_parsed", "photo", "photo_parsed", 
                 "category_avg_goal", "country_success_rate"]
    df_final.drop(columns=[c for c in drop_cols if c in df_final.columns], inplace=True)
    
    # Separate X and y
    y = df_final[TARGET_COL] if TARGET_COL in df_final.columns else pd.Series([0] * len(df_final))
    X = df_final.drop(columns=[TARGET_COL], errors="ignore")
    
    # Force numeric & fill NaN, but preserve datetime and text columns
    datetime_cols = [c for c in X.columns if pd.api.types.is_datetime64_any_dtype(X[c])]
    text_cols = ["name", "blurb", "country", "currency", "currency_symbol", "category"]
    non_numeric_cols = datetime_cols + text_cols
    numeric_cols = [c for c in X.columns if c not in non_numeric_cols]
    
    # Convert numeric columns to numeric
    X_numeric = X[numeric_cols].apply(
        lambda col: pd.to_numeric(col, errors="coerce") if col.dtype == "object" else col
    )
    X_numeric = X_numeric.fillna(0)
    
    # Combine back with non-numeric columns
    X = pd.concat([X_numeric, X[non_numeric_cols]], axis=1)
    
    target_encoders["global_mean"] = float(y.mean())
    
    print(f"Final dataset prepared. Features: {X.shape[1]}")
    return X, y, target_encoders

# ---------------------------
# 5. Train/val/test split
# ---------------------------
def manual_train_test_split(X, y, test_size=0.2, val_size=0.1, random_state=42):
    random.seed(random_state)
    np.random.seed(random_state)
    n = len(X)
    indices = list(range(n))
    random.shuffle(indices)
    
    test_end = int(test_size * n)
    val_end = test_end + int(val_size * n)
    
    test_idx = indices[:test_end]
    val_idx = indices[test_end:val_end]
    train_idx = indices[val_end:]
    
    return (X.iloc[train_idx], X.iloc[val_idx], X.iloc[test_idx],
            y.iloc[train_idx], y.iloc[val_idx], y.iloc[test_idx])

def manual_standard_scaler(X_train, X_val, X_test):
    # Separate datetime and text columns from numeric columns
    datetime_cols = [c for c in X_train.columns if pd.api.types.is_datetime64_any_dtype(X_train[c])]
    text_cols = ["name", "blurb", "country", "currency", "currency_symbol", "category"]
    non_numeric_cols = datetime_cols + text_cols
    numeric_cols = [c for c in X_train.columns if c not in non_numeric_cols]
    
    # Scale only numeric columns
    X_train_numeric = X_train[numeric_cols].astype(float).to_numpy()
    X_val_numeric = X_val[numeric_cols].astype(float).to_numpy()
    X_test_numeric = X_test[numeric_cols].astype(float).to_numpy()
    
    mean_train = np.nanmean(X_train_numeric, axis=0)
    std_train = np.nanstd(X_train_numeric, axis=0)
    std_train = np.where(std_train == 0, 1, std_train)
    
    X_train_scaled_numeric = (np.nan_to_num(X_train_numeric - mean_train) / std_train)
    X_val_scaled_numeric = (np.nan_to_num(X_val_numeric - mean_train) / std_train)
    X_test_scaled_numeric = (np.nan_to_num(X_test_numeric - mean_train) / std_train)
    
    # Convert back to DataFrames
    X_train_scaled = pd.DataFrame(X_train_scaled_numeric, columns=numeric_cols, index=X_train.index)
    X_val_scaled = pd.DataFrame(X_val_scaled_numeric, columns=numeric_cols, index=X_val.index)
    X_test_scaled = pd.DataFrame(X_test_scaled_numeric, columns=numeric_cols, index=X_test.index)
    
    # Add back non-numeric columns
    for col in non_numeric_cols:
        if col in X_train.columns:
            X_train_scaled[col] = X_train[col]
            X_val_scaled[col] = X_val[col]
            X_test_scaled[col] = X_test[col]
    
    return X_train_scaled, X_val_scaled, X_test_scaled, mean_train, std_train

# ---------------------------
# 6. Full preprocessing pipeline
# ---------------------------
def full_preprocessing_pipeline(filepath):
    df = load_data(filepath)
    df_clean = clean_data(df)
    df_feat = engineer_features(df_clean)
    X, y, encoders = encode_and_prepare(df_feat)
    
    X_train, X_val, X_test, y_train, y_val, y_test = manual_train_test_split(X, y)
    X_train_scaled, X_val_scaled, X_test_scaled, mean_train, std_train = manual_standard_scaler(X_train, X_val, X_test)
    
    encoders["scaler_mean"] = mean_train.tolist()
    encoders["scaler_std"] = std_train.tolist()
    
    return X_train_scaled, X_val_scaled, X_test_scaled, y_train, y_val, y_test, encoders

# ---------------------------
# 7. Run pipeline
# ---------------------------
def run_preprocessing():
    print("🚀 Starting preprocessing pipeline...")
    
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    raw_path = os.path.join(root_dir, "data", "raw", "kickstarter_data_full.csv")
    processed_path = os.path.join(root_dir, "data", "processed", "processed.csv")
    readable_path = os.path.join(root_dir, "data", "processed", "processed_readable.csv")
    
    X_train, X_val, X_test, y_train, y_val, y_test, encoders = full_preprocessing_pipeline(raw_path)
    
    # Save processed dataframe for modeling (normalized)
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    
    # Create column names for the processed data
    feature_names = X_train.columns.tolist()
    
    # Save training data (normalized)
    pd.concat([
        pd.DataFrame(X_train, columns=feature_names), 
        y_train.reset_index(drop=True)
    ], axis=1).to_csv(processed_path, index=False)
    
    # Save validation and test data (normalized)
    val_path = processed_path.replace(".csv", "_val.csv")
    test_path = processed_path.replace(".csv", "_test.csv")
    
    pd.concat([
        pd.DataFrame(X_val, columns=feature_names), 
        y_val.reset_index(drop=True)
    ], axis=1).to_csv(val_path, index=False)
    
    pd.concat([
        pd.DataFrame(X_test, columns=feature_names), 
        y_test.reset_index(drop=True)
    ], axis=1).to_csv(test_path, index=False)
    
    # Save a human-readable version (not normalized)
    # First, let's recreate the feature names from the engineering step
    df = load_data(raw_path)
    df_clean = clean_data(df)
    df_feat = engineer_features(df_clean)
    X_readable, y_readable, _ = encode_and_prepare(df_feat, is_training=True)
    
    # Save readable version
    readable_df = pd.concat([X_readable, y_readable], axis=1)
    readable_df.to_csv(readable_path, index=False)
    
    # Save encoders for later use in prediction
    encoders_path = os.path.join(root_dir, "data", "processed", "encoders.npy")
    np.save(encoders_path, encoders, allow_pickle=True)
    
    # Also save feature names for reference
    feature_names_path = os.path.join(root_dir, "data", "processed", "feature_names.txt")
    with open(feature_names_path, 'w') as f:
        for i, name in enumerate(feature_names):
            f.write(f"{i}: {name}\n")
    
    print(f"✅ Preprocessing complete. Processed data saved to {processed_path}")
    print(f"Readable data saved to {readable_path}")
    print(f"Encoders saved to {encoders_path}")
    print(f"Feature names mapping saved to {feature_names_path}")
    
    return X_train, X_val, X_test, y_train, y_val, y_test, encoders

if __name__ == "__main__":
    run_preprocessing()