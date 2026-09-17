import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error

# --- PREPROCESSING & LOADING ---
def run_pipeline():
    print("--- 1. Data Loading & Preprocessing ---")
    data_path = 'data/crop_yield.csv'
    
    if not os.path.exists(data_path):
        print(f"Error: Dataset not found at {data_path}")
        return

    df = pd.read_csv(data_path)
    df.columns = df.columns.str.strip().str.lower()
    df = df.dropna()
    print(f"Loaded data. Removed missing rows.")

    # Define Features and Target
    features = ['fertilizer', 'temp', 'n', 'p', 'k']
    target = 'yeild'
    
    X = df[features]
    y = df[target]

    # --- 2. Model Training & Comparison ---
    print("\n--- 2. Model Training & Comparison ---")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model 1: Linear Regression (Baseline)
    from sklearn.linear_model import LinearRegression
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    lr_preds = lr_model.predict(X_test)
    lr_r2 = r2_score(y_test, lr_preds)
    print(f"Linear Regression R2 Score: {lr_r2:.4f}")

    # Model 2: Gradient Boosting (Current Engine)
    gb_model = GradientBoostingRegressor(
        n_estimators=150, 
        learning_rate=0.1, 
        max_depth=5, 
        random_state=42
    )
    gb_model.fit(X_train, y_train)
    gb_preds = gb_model.predict(X_test)
    gb_r2 = r2_score(y_test, gb_preds)
    print(f"Gradient Boosting R2 Score: {gb_r2:.4f}")

    # --- 3. Visualization ---
    print("\n--- 3. Generating Performance Comparison ---")
    plt.figure(figsize=(12, 5))
    
    # Linear Regression Plot
    plt.subplot(1, 2, 1)
    plt.scatter(y_test, lr_preds, alpha=0.5, color='#3b82f6')
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.title(f"Baseline: Linear Regression\n(R2: {lr_r2:.4f})")
    plt.xlabel("Actual Yield")
    plt.ylabel("Predicted Yield")

    # Gradient Boosting Plot
    plt.subplot(1, 2, 2)
    plt.scatter(y_test, gb_preds, alpha=0.5, color='#10b981')
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.title(f"Engine: Gradient Boosting\n(R2: {gb_r2:.4f})")
    plt.xlabel("Actual Yield")
    plt.ylabel("Predicted Yield")

    plt.tight_layout()
    plt.savefig('models/model_comparison.png')
    print("Comparison plot saved to models/model_comparison.png")

    # --- SAVING THE MODEL ---
    joblib.dump(gb_model, 'models/crop_yield_model.pkl')
    print(f"\nPipeline Complete! Model saved to models/crop_yield_model.pkl")

if __name__ == "__main__":
    run_pipeline()
