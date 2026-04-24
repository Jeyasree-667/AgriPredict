import joblib
import pandas as pd
import numpy as np

model = joblib.load('models/crop_yield_model.pkl')
features = ['fertilizer', 'temp', 'n', 'p', 'k']

# Test Case 1: Standard Values
test1 = pd.DataFrame([[80.0, 28, 80.0, 24.0, 20.0]], columns=features)
# Test Case 2: high fertilizer
test2 = pd.DataFrame([[500.0, 28, 80.0, 24.0, 20.0]], columns=features)
# Test Case 3: low temperature
test3 = pd.DataFrame([[80.0, 10, 80.0, 24.0, 20.0]], columns=features)
# Test Case 4: low nutrients
test4 = pd.DataFrame([[80.0, 28, 10.0, 5.0, 5.0]], columns=features)

print(f"Test 1 (Standard): {model.predict(test1)[0]}")
print(f"Test 2 (High Fert): {model.predict(test2)[0]}")
print(f"Test 3 (Low Temp): {model.predict(test3)[0]}")
print(f"Test 4 (Low Nutrients): {model.predict(test4)[0]}")

if hasattr(model, 'feature_importances_'):
    print("\nFeature Importances:")
    for f, imp in zip(features, model.feature_importances_):
        print(f"{f}: {imp:.4f}")
