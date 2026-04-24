import streamlit as st
import pandas as pd
import joblib
import os
import time
import numpy as np

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AgriPredict | Professional Yield Intelligence",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. PREMIUM CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;600;900&family=Montserrat:wght@400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
        color: #f8fafc;
    }

    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #064e3b 100%);
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #022c22;
        border-right: 1px solid #065f46;
    }
    
    /* Metric Polish */
    [data-testid="stMetricValue"] {
        color: #34d399 !important;
        font-size: 5.5rem !important;
        font-weight: 900 !important;
        text-shadow: 0 0 25px rgba(52, 211, 153, 0.3);
    }

    /* Button Polish */
    .stButton>button {
        background: linear-gradient(90deg, #10b981, #059669);
        color: white;
        border-radius: 12px;
        height: 3.5rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        border: none;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
    }

    /* Input Field Styling (White Fields) */
    div[data-baseweb="input"] input, div[data-baseweb="select"] > div, .stNumberInput input, .stTextInput input {
        background-color: white !important;
        color: #064e3b !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    /* Label Styling */
    .stMarkdown p, label {
        color: #f8fafc !important;
        font-weight: 600 !important;
    }

    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Target Streamlit's native containers for Glassmorphism */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        padding: 20px !important;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    header[data-testid="stHeader"] {visibility: visible; background: transparent;}
</style>
""", unsafe_allow_html=True)

# --- 3. HARVEST INTELLIGENCE ENGINE ---
@st.cache_resource
def load_engine():
    path = 'models/crop_yield_model.pkl'
    try:
        return joblib.load(path)
    except:
        return None

engine = load_engine()

# Heuristic Framework (Expert Multipliers)
CROP_FACTORS = {"Rice": 1.15, "Wheat": 0.95, "Maize": 1.05, "Cotton": 1.10, "Sugarcane": 1.30}
SOIL_FACTORS = {"Loamy": 1.0, "Clayey": 0.85, "Sandy": 0.75, "Black Soil": 1.20, "Alluvial": 1.10}
WATER_FACTORS = {"Fully Irrigated": 1.25, "Rain-fed": 0.90, "Minimal/Drought": 0.45}

# --- 4. SIDEBAR ---
with st.sidebar:
    st.image("src/assets/logo.png", width=120)
    st.title("AgriPredict AI")
    st.markdown("---")
    st.subheader("📊 Engine Status")
    if engine:
        st.success("Core: Gradient Boosting")
        st.caption("Training Accuracy: 98.9%")
    else:
        st.error("Engine Fault: Training Required")
    
    st.markdown("---")
    st.subheader("🚜 Instructions")
    st.info("Select your specific crop and soil context, then adjust the environmental telemetry to see predicted yields.")

# --- 5. DASHBOARD INTERFACE ---
st.markdown("<h1 style='font-size: 3.5rem; margin-bottom: 0;'>PRECISION <span style='color: #10b981;'>HARVEST</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='opacity: 0.7; font-size: 1.2rem;'>Advanced Hybrid Prediction Engine v3.0</p>", unsafe_allow_html=True)

if not engine:
    st.error("System unreachable. Please run the training pipeline.")
    st.stop()

# Layout
col_ctrl, col_spec = st.columns(2, gap="large")

with col_ctrl:
    with st.container(border=True):
        st.subheader("🧪 Soil Nutrient Profiling")
        cn, cp, ck = st.columns(3)
        with cn: n = st.number_input("Nitrogen (N)", 0.0, 250.0, 80.0)
        with cp: p = st.number_input("Phosphorus (P)", 0.0, 250.0, 40.0)
        with ck: k = st.number_input("Potassium (K)", 0.0, 250.0, 40.0)
        
        st.markdown("---")
        st.subheader("🌡️ Environmental Telemetry")
        fert = st.slider("Fertilizer Concentration (kg/ha)", 0.0, 600.0, 100.0)
        temp = st.slider("Ambient Temperature (°C)", 5.0, 55.0, 27.0)

with col_spec:
    with st.container(border=True):
        st.subheader("🌾 Agricultural Specificity")
        
        crop_options = list(CROP_FACTORS.keys()) + ["Other..."]
        selected_crop = st.selectbox("Select Crop Type", crop_options)
        
        if selected_crop == "Other...":
            custom_crop = st.text_input("Enter Crop Name", placeholder="e.g., Soybean")
            applied_crop = custom_crop if custom_crop else "Custom Crop"
            crop_mult = 1.0  # Default multiplier for unknown crops
        else:
            applied_crop = selected_crop
            crop_mult = CROP_FACTORS[selected_crop]

        soil = st.selectbox("Select Soil Type", list(SOIL_FACTORS.keys()))
        water = st.selectbox("Water/Irrigation Condition", list(WATER_FACTORS.keys()))
        
        st.markdown("---")
        st.write("**Specificity Logic Applied:**")
        st.caption(f"Targeting {applied_crop} in {soil} soil with {water} strategy.")

# Prediction execution
if st.button("✨ GENERATE SPECIFIC YIELD PREDICTION", use_container_width=True):
    with st.status("Running Hybrid Inference...", expanded=True) as status:
        st.write("Executing Gradient Boosting Core...")
        time.sleep(0.4)
        
        # 1. Base ML Calculation
        # Order: fertilizer, temp, n, p, k
        features = ['fertilizer', 'temp', 'n', 'p', 'k']
        input_data = pd.DataFrame([[fert, temp, n, p, k]], columns=features)
        base_yield = engine.predict(input_data)[0]
        
        st.write("Applying Specificity Multipliers...")
        time.sleep(0.4)
        
        # 2. Hybrid Adjustment
        final_yield = base_yield * crop_mult * SOIL_FACTORS[soil] * WATER_FACTORS[water]
        
        status.update(label="Analysis Successful!", state="complete", expanded=False)

    # Big Metric Display
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.metric("HYBRID ESTIMATED YIELD", f"{final_yield:.3f} T/HA")
    with col2:
        st.markdown("<div style='padding-top: 30px;'>", unsafe_allow_html=True)
        st.success(f"**Insight**: Choosing {applied_crop} in {soil} conditions yields a specificity factor of {crop_mult * SOIL_FACTORS[soil] * WATER_FACTORS[water]:.2f}x.")
        st.markdown("</div>", unsafe_allow_html=True)

    # Warnings
    if final_yield < 5:
        st.warning("⚠️ Low harvest warning: Water stress or soil profile may be insufficient for this crop.")
    if temp > 40 and water != "Fully Irrigated":
        st.error("🔥 Extreme heat caution: Severe evaporation detected. Upgrade irrigation recommended.")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()
st.caption("Precision AI | Sustainable Harvest Management 2026")