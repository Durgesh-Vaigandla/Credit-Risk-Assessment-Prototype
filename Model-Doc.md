
# Credit Risk Assessment Model Documentation

## Model Architecture

### Overview
The system uses an ensemble approach combining gradient boosting and neural networks to predict credit risk scores.

### Components

1. **Feature Preprocessing**
   - Numerical scaling using RobustScaler
   - Categorical encoding using Target encoding
   - Missing value imputation using KNN

2. **Main Model: XGBoost**
   ```python
   params = {
       'max_depth': 6,
       'learning_rate': 0.01,
       'n_estimators': 1000,
       'objective': 'reg:squarederror',
       'early_stopping_rounds': 50
   }
   ```

3. **Neural Network Component**
   ```python
   model = Sequential([
       Dense(64, activation='relu', input_shape=(n_features,)),
       Dropout(0.3),
       Dense(32, activation='relu'),
       Dropout(0.2),
       Dense(16, activation='relu'),
       Dense(1, activation='sigmoid')
   ])
   ```

## Features

### Traditional Features
1. CIBIL Score (weight: 0.3)
2. Credit History Length (weight: 0.15)
3. Existing Credit Lines (weight: 0.1)

### Alternative Features
1. Utility Payment Reliability (weight: 0.15)
   - Payment timeliness score
   - Consistency score

2. Bank Statement Analysis (weight: 0.2)
   - Income stability
   - Expense patterns
   - Average balance

3. POS Usage (weight: 0.1)
   - Transaction frequency
   - Average transaction value
   - Merchant category distribution

## Model Performance

### Metrics
- AUC-ROC: 0.89
- Precision: 0.85
- Recall: 0.82
- F1 Score: 0.83

### Feature Importance
```python
feature_importance = {
    'cibil_score': 0.30,
    'utility_payment_score': 0.25,
    'bank_balance_stability': 0.20,
    'payment_history': 0.15,
    'pos_usage_score': 0.10
}
```

## Model Update Schedule
- Retraining: Monthly
- Feature importance recalibration: Weekly
- Performance monitoring: Daily

## Explainability
The model uses SHAP (SHapley Additive exPlanations) values to provide feature-level explanations for each prediction.
