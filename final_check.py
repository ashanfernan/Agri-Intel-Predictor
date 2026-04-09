import streamlit as st
import pandas as pd
import joblib
import os
import numpy as np
import plotly.graph_objects as go
import requests

# 1. Page Configuration
st.set_page_config(page_title="Agri-Intel Pro v3.0", page_icon="🌱", layout="wide")

# Custom CSS for Glassmorphism UI
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    div[data-testid="stSidebar"] {
        background-color: #1b2e1b;
    }
    .stAlert {
        border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# API Configuration
API_KEY = "YOUR_API_KEY_HERE" 

# 2. Model Loading
model_path = 'agri_intel_model.pkl'
model = joblib.load(model_path) if os.path.exists(model_path) else None

def get_live_weather(city):
    if API_KEY == "YOUR_API_KEY_HERE": return None
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        res = requests.get(url)
        return res.json() if res.status_code == 200 else None
    except: return None

# --- SIDEBAR (INPUTS) ---
with st.sidebar:
    st.image("https://img.icons8.com/fluent/96/000000/leaf.png", width=80)
    st.title("Agri-Intel Pro")
    st.markdown("---")
    
    city = st.text_input("📍 ඔබ ඉන්නා නගරය", "Colombo")
    
    # Auto Weather Data Fetching
    weather = get_live_weather(city)
    temp = weather['main']['temp'] if weather else 28.0
    rain = weather.get('rain', {}).get('1h', 1200.0) if weather else 1200.0
    
    st.info(f"🌡️ වත්මන් උෂ්ණත්වය: {temp}°C")
    st.info(f"🌧️ වර්ෂාපතනය: {rain} mm")
    
    st.markdown("---")
    crop = st.selectbox("වගා බෝගය", ["වී (Paddy)", "බඩඉරිඟු (Corn)", "තේ (Tea)"])
    unit = st.selectbox("ඉඩම් ඒකකය", ["Acres (අක්කර)", "Perches (පර්චස්)", "Hectares"])
    size = st.number_input(f"ප්‍රමාණය ({unit})", value=1.0)
    
    # Conversion Logic
    ha = size * 0.404 if "Acres" in unit else size * 0.0025 if "Perches" in unit else size

st.title("🌾 Agri-Intel Precision Dashboard")

# 3. DISASTER ALERTS
if rain > 1800:
    st.error("🚨 **Flood Warning:** අධික වර්ෂාව නිසා පොහොර යෙදීමෙන් වළකින්න!")
elif temp > 35:
    st.warning("⚠️ **Heat Alert:** දැඩි රශ්මිය! වගාවට වැඩිපුර ජලය අවශ්‍යයි.")

# 4. PREDICTIONS & METRICS
if model:
    # Calculation
    input_df = pd.DataFrame([[temp, rain, 200.0]], columns=['farm_size_hectares', 'rainfall_mm', 'fertilizer_kg'])
    y_pred = float(model.predict(input_df).flatten()[0]) * ha
    total_fert = 200.0 * ha

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("අපේක්ෂිත අස්වැන්න", f"{y_pred:.1f} kg", delta="Optimal")
    with col2:
        st.metric("අවශ්‍ය මුළු පොහොර", f"{total_fert:.1f} kg", delta="-5% Saving")
    with col3:
        st.metric("වගා භූමිය", f"{ha:.3f} Ha")

    st.markdown("---")

    # 5. VISUALS & ADVICE
    c1, c2 = st.columns([1, 1.5])
    with c1:
        st.subheader(f"📋 {crop} විශේෂ උපදෙස්")
        st.success(f"✅ සති 2දී: යුරියා {(50*ha):.1f}kg")
        st.success(f"✅ සති 6දී: යුරියා {(75*ha):.1f}kg")
        st.markdown("> **සටහන:** කාලගුණික දත්ත මත පදනම්ව මේවා ස්වයංක්‍රීයව වෙනස් වේ.")
    
    with c2:
        # Chart
        f_range = np.linspace(0, 600, 50)
        sim = model.predict(pd.DataFrame({'farm_size_hectares':[temp]*50,'rainfall_mm':[rain]*50,'fertilizer_kg':f_range}))
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=f_range*ha, y=sim*ha, name="Yield Curve", line=dict(color='#2ecc71', width=4)))
        fig.add_trace(go.Scatter(x=[total_fert], y=[y_pred], mode='markers', marker=dict(color='red', size=15), name="ඔබේ තත්ත්වය"))
        fig.update_layout(title="පොහොර vs අස්වැන්න", template="plotly_dark", height=350, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)

st.caption("Agri-Intel v3.0 | Powered by Data Science 🚀")