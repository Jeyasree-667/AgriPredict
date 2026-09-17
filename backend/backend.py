import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Heuristic Framework (Expert Multipliers)
CROP_FACTORS = {"Rice": 1.15, "Wheat": 0.95, "Maize": 1.05, "Cotton": 1.10, "Sugarcane": 1.30, "Other...": 1.0}
SOIL_FACTORS = {"Loamy": 1.0, "Clayey": 0.85, "Sandy": 0.75, "Black Soil": 1.20, "Alluvial": 1.10}
WATER_FACTORS = {"Fully Irrigated": 1.25, "Rain-fed": 0.90, "Minimal/Drought": 0.45}

def load_engine():
    path = os.path.join(os.path.dirname(__file__), 'models', 'crop_yield_model.pkl')
    try:
        return joblib.load(path)
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

engine = load_engine()

@app.route('/api/predict', methods=['POST'])
def predict():
    if engine is None:
        return jsonify({'error': 'Prediction engine offline. Training required.'}), 503

    try:
        data = request.json
        
        # Environmental and Soil Data
        fert = float(data.get('fertilizer', 100))
        temp = float(data.get('temperature', 27))
        n = float(data.get('n', 80))
        p = float(data.get('p', 40))
        k = float(data.get('k', 40))
        
        # Specificity
        crop = data.get('crop', 'Rice')
        soil = data.get('soil', 'Loamy')
        water = data.get('water', 'Fully Irrigated')
        
        crop_mult = CROP_FACTORS.get(crop, 1.0)
        soil_mult = SOIL_FACTORS.get(soil, 1.0)
        water_mult = WATER_FACTORS.get(water, 1.0)
        
        # Base ML Calculation
        features = ['fertilizer', 'temp', 'n', 'p', 'k']
        input_data = pd.DataFrame([[fert, temp, n, p, k]], columns=features)
        base_yield = engine.predict(input_data)[0]
        
        # Hybrid Adjustment
        specificity_factor = crop_mult * soil_mult * water_mult
        final_yield = base_yield * specificity_factor
        
        # Warnings logic
        warnings = []
        if final_yield < 5:
            warnings.append("Low harvest warning: Water stress or soil profile may be insufficient for this crop.")
        if temp > 40 and water != "Fully Irrigated":
            warnings.append("Extreme heat caution: Severe evaporation detected. Upgrade irrigation recommended.")

        return jsonify({
            'success': True,
            'base_yield': float(base_yield),
            'final_yield': float(final_yield),
            'specificity_factor': float(specificity_factor),
            'warnings': warnings
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({
        'engine_online': engine is not None,
        'crop_options': list(CROP_FACTORS.keys()),
        'soil_options': list(SOIL_FACTORS.keys()),
        'water_options': list(WATER_FACTORS.keys())
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
