# 🌱 AgriPredict AI | Precision Yield Intelligence

AgriPredict is a high-fidelity machine learning dashboard designed for sustainable harvest management. It uses a **hybrid approach**, combining a Gradient Boosting machine learning model with an expert heuristic framework to provide highly specific crop yield estimates based on environmental conditions and soil nutrients.

## 🚀 Features

- **Hybrid Prediction Engine**: Integrates a trained `GradientBoostingRegressor` with expert agricultural multipliers.
- **Micro-Nutrient Profiling**: Analyzes Nitrogen (N), Phosphorus (P), and Potassium (K) levels.
- **Environmental Telemetry**: Accounts for temperature and fertilizer concentration.
- **Agricultural Specificity**: High-precision adjustments for diverse crop types (Rice, Wheat, Maize, etc.), soil textures (Loamy, Clayey, etc.), and irrigation strategies.
- **Premium UI**: A completely custom, modern frontend built with HTML/CSS/JS, featuring a dark-mode glassmorphism aesthetic and dynamic animations.
- **API Backend**: A lightweight Flask API that serves the machine learning model predictions.

## 🧠 Technical Flow (End-to-End)

1. **Data Collection (Frontend)**: The user inputs numerical and categorical data via the HTML/CSS web interface.
2. **Network Transmission**: The `app.js` frontend script sends an asynchronous JSON POST request to the Flask backend endpoint (`/api/predict`).
3. **Core ML Inference (Backend)**: Flask parses the 5 numerical features (N, P, K, Fertilizer, Temp) into a Pandas DataFrame and feeds it to the pre-loaded Gradient Boosting model (`crop_yield_model.pkl`) to calculate a **Base Yield**.
4. **Hybrid Heuristic Engine**: The backend extracts categorical data (Crop, Soil, Water) and maps them to predefined multiplier dictionaries to calculate a **Specificity Factor**. The **Final Yield** is the Base Yield multiplied by this factor.
5. **Business Logic & Guardrails**: The backend checks for thresholds (e.g., Yield < 5, Temp > 40) and appends relevant warnings to the response.
6. **UI Hydration**: The frontend receives the JSON response, animates the final yield number on the screen, and dynamically renders warning cards.

## 🛠️ Tech Stack

- **Backend Logic & API**: Python 3.x, Flask, Flask-CORS
- **Inference Engine**: Scikit-Learn (Gradient Boosting), Pandas, Joblib
- **Frontend UI**: Vanilla HTML, CSS, JavaScript (No frameworks)

## 📂 Project Structure

```text
ML_MINI/
├── backend/
│   ├── backend.py              # Flask API Server
│   ├── ml_pipeline.py          # Training & Evaluation Pipeline
│   └── models/
│       └── crop_yield_model.pkl # Trained ML Model
├── frontend/
│   ├── index.html              # Dashboard Structure
│   ├── styles.css              # Premium Styling
│   ├── app.js                  # Frontend Logic & API calls
│   └── assets/                 # Images/Logos
├── src/
│   └── test_model.py           # CLI Validation Scripts
├── data/
│   └── crop_yield.csv          # Raw Agricultural Dataset
├── archive/                    # Archived Streamlit files
├── requirements.txt            # Python Dependencies
└── README.md
```

## ⚙️ Installation & Running the Application

This application uses a decoupled architecture. You will need to run the backend and the frontend separately.

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Backend API (Terminal 1)
```bash
cd backend
python backend.py
```
*(The backend will start running on port 5000)*

### 3. Start the Frontend UI (Terminal 2)
```bash
cd frontend
python -m http.server 8000
```
*(You can now open your browser and navigate to **http://localhost:8000**)*
> **Note**: Alternatively, you can simply open the `frontend/index.html` file directly in your web browser.

---
*Precision AI | Sustainable Harvest Management 2026*
