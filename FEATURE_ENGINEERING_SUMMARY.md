# Feature Engineering Summary

## Dataset Statistics

### Raw Dataset
- **Total Columns:** 68
- **Total Rows:** 20,632 campaigns

### Processed Dataset (After Feature Engineering)
- **Total Columns:** 71
- **Total Rows:** 18,747 campaigns (after removing invalid/incomplete records)

### Feature Engineering Impact
- **Original Features:** 68
- **Engineered Features (NEW):** 25
- **Removed Features:** 22
- **Final Features:** 71 total (46 original + 25 engineered)

---

## 25 Engineered Features (Created by Us)

### 1. Currency Normalization (1 feature)
- **`goal_usd`** - Goal converted to USD for fair comparison

### 2. Duration Risk Indicators (2 features)
- **`duration_risk_short`** - Flag for campaigns < 7 days (too short)
- **`duration_risk_long`** - Flag for campaigns > 90 days (too long)

### 3. Launch Timing Features (5 features)
- **`launch_hour`** - Hour of day when launched (0-23)
- **`launch_weekday`** - Day of week when launched (0-6)
- **`launch_month`** - Month when launched (1-12)
- **`launch_is_weekend`** - Binary flag for weekend launches
- **`launched_tuesday`** - Binary flag for Tuesday launches (optimal day)

### 4. Text Analysis Features (7 features)
- **`name_clean`** - Cleaned/lowercased campaign name
- **`blurb_clean`** - Cleaned/lowercased description
- **`blurb_exclaims`** - Count of exclamation marks
- **`blurb_positive_score`** - Count of positive sentiment words
- **`blurb_negative_score`** - Count of negative sentiment words
- **`text_sentiment_score`** - Net sentiment (positive - negative)
- **`text_quality_score`** - Combined quality metric: (positive×2 + length/100) - negative

### 5. Creator Profile Features (4 features)
- **`creator_has_avatar`** - Binary flag for profile completeness
- **`creator_id`** - Extracted creator ID
- **`creator_project_count`** - Number of campaigns by this creator
- **`creator_reputation`** - Log-transformed experience: log(1 + project_count)

### 6. Media Features (1 feature)
- **`photo_count`** - Number of images in campaign

### 7. Benchmark Features (1 feature)
- **`goal_vs_category_benchmark`** - Goal relative to category average (ratio)

### 8. Target Encoding (4 features)
- **`category_te`** - Category encoded by success rate
- **`country_te`** - Country encoded by success rate
- **`currency_te`** - Currency encoded by success rate
- **`currency_symbol_te`** - Currency symbol encoded by success rate

---

## 22 Removed Features (Data Leakage + Useless)

### Data Leakage Features (11 features) - Known Only AFTER Campaign Ends
1. **`pledged`** - Money raised (this IS the outcome!)
2. **`usd_pledged`** - Money raised in USD
3. **`backers_count`** - Number of backers (outcome variable)
4. **`state_changed_at`** - When campaign ended
5. **`state_changed_at_hr`** - Hour campaign ended
6. **`state_changed_at_weekday`** - Weekday campaign ended
7. **`launch_to_state_change`** - Duration to campaign end
8. **`launch_to_state_change_days`** - Days to campaign end
9. **`spotlight`** - Editorial feature (assigned during campaign based on performance)
10. **`staff_pick`** - Editorial feature (assigned during campaign based on performance)

### Useless/Redundant Features (11 features)
11. **`Unnamed: 0`** - Index column
12. **`slug`** - URL slug (not predictive)
13. **`urls`** - URLs (not predictive)
14. **`source_url`** - Source URL (not predictive)
15. **`friends`** - Friend data (not available at launch)
16. **`permissions`** - Permission data (not predictive)
17. **`profile`** - Profile JSON (parsed into features)
18. **`location`** - Location JSON (redundant with country)
19. **`is_starred`** - User-specific (not predictive)
20. **`is_backing`** - User-specific (not predictive)
21. **`creator`** - Creator JSON (parsed into creator_* features)
22. **`photo`** - Photo JSON (parsed into photo_count)

---

## Final Feature Set (71 Total)

### Breakdown by Source:
- **Original Features (kept):** 46
  - Campaign basics: goal, currency, country, category
  - Datetime features: deadline, created_at, launched_at
  - Pre-computed: name_len, blurb_len, deadline_weekday, etc.
  - Flags: disable_communication, USorGB, TOPCOUNTRY, etc.

- **Engineered Features (created):** 25
  - Currency: goal_usd
  - Duration risk: duration_risk_short, duration_risk_long
  - Launch timing: launch_hour, launch_weekday, launch_month, etc.
  - Text analysis: sentiment scores, quality scores
  - Creator profile: has_avatar, project_count, reputation
  - Media: photo_count
  - Benchmarks: goal_vs_category_benchmark
  - Target encoding: category_te, country_te, etc.

---

## Feature Engineering Techniques Applied

### 1. **Temporal Feature Extraction**
```python
# From datetime → multiple features
launched_at → launch_hour, launch_weekday, launch_month, launch_is_weekend
```

### 2. **Text Mining & NLP**
```python
# Sentiment analysis
positive_words = ["amazing", "innovative", "exciting", ...]
blurb_positive_score = count(positive_words in blurb)
text_sentiment_score = positive_score - negative_score
```

### 3. **Aggregation Features**
```python
# Group statistics
creator_project_count = count of campaigns per creator
goal_vs_category_benchmark = goal / mean(goal per category)
```

### 4. **Target Encoding**
```python
# Encode categories by target mean
category_te = mean(success_rate) for each category
country_te = mean(success_rate) for each country
```

### 5. **Log Transformation**
```python
# Handle skewed distributions
creator_reputation = log(1 + creator_project_count)
```

### 6. **Binary Flags**
```python
# Threshold-based indicators
duration_risk_short = 1 if duration < 7 else 0
launch_is_weekend = 1 if weekday in [5,6] else 0
```

### 7. **Ratio Features**
```python
# Relative metrics
goal_vs_category_benchmark = goal_usd / category_avg_goal
```

---

## Data Leakage Prevention

### Why We Removed These Features:

**Problem:** Initial training showed 100% accuracy (too good to be true!)

**Root Cause:** Data leakage from outcome variables

**Features Removed:**
1. **Direct Outcomes:** pledged, usd_pledged, backers_count
   - These ARE the answer - only known after campaign ends

2. **Campaign End Timing:** state_changed_at, launch_to_state_change_days
   - Only known after campaign completes

3. **Editorial Features:** spotlight, staff_pick
   - Assigned DURING campaign based on performance
   - Reverse causation: success → spotlight (not spotlight → success)

**Result:**
- Before removal: 100% accuracy (cheating)
- After removal: 70-75% accuracy (realistic)

---

## For Presentation

### Key Talking Points:

**Q: How many features did you engineer?**
**A:** We created **25 new features** from the original 68 columns:
- 7 text analysis features (sentiment, quality)
- 5 launch timing features (hour, weekday, month)
- 4 creator profile features (experience, reputation)
- 4 target encoding features (category, country success rates)
- 2 duration risk indicators
- 1 currency normalization
- 1 media feature (photo count)
- 1 benchmark feature (goal vs category)

**Q: What happened to the original features?**
**A:** 
- **Kept:** 46 original features (campaign basics, dates, flags)
- **Removed:** 22 features (11 data leakage + 11 useless/redundant)
- **Created:** 25 engineered features
- **Final:** 71 total features

**Q: Why did you remove 22 features?**
**A:** 
1. **Data Leakage (11):** Features only known AFTER campaign ends
   - Example: pledged amount, backers_count, spotlight
   - These gave 100% accuracy but were "cheating"

2. **Useless/Redundant (11):** Not predictive or already captured
   - Example: URLs, JSON blobs (parsed into features), user-specific flags

**Q: What techniques did you use?**
**A:**
1. Temporal extraction (hour, weekday, month from timestamps)
2. Text mining & sentiment analysis (positive/negative word counts)
3. Aggregation (creator project count, category benchmarks)
4. Target encoding (encode categories by success rate)
5. Log transformation (handle skewed distributions)
6. Binary flags (weekend, duration risk)
7. Ratio features (goal vs category average)

---

## Impact on Model Performance

### Before Data Leakage Removal:
- Decision Tree: **100% accuracy** (unrealistic)
- Top feature: spotlight (10% importance)

### After Data Leakage Removal:
- Decision Tree: **75% accuracy** (realistic)
- Random Forest: **72% accuracy, 53% F1-score**
- Top features: goal_usd, launch_to_deadline_days, creator_reputation

**Conclusion:** Proper feature engineering and leakage prevention resulted in realistic, production-ready models.
