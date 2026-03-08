import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load the model (උඹේ මොඩලය මෙතැනදී Load වෙනවා)
def load_model():
    with open('model.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

# UI එක ලස්සනට හදමු
st.set_page_config(page_title="Agri-Intel Pro", layout="wide")
st.title("🌱 Agri-Intel: Smart Yield Predictor & Advisor")
st.markdown("---")

# Sidebar එකේ Sliders දාමු
st.sidebar.header("අවශ්‍ය දත්ත ඇතුළත් කරන්න")
rainfall = st.sidebar.slider("සාමාන්‍ය වර්ෂාපතනය (mm)", 50.0, 3500.0, 1100.0)
temp = st.sidebar.slider("සාමාන්‍ය උෂ්ණත්වය (°C)", 10.0, 50.0, 25.0)
pesticides = st.sidebar.slider("පළිබෝධනාශක ප්‍රමාණය (tonnes)", 0.0, 50000.0, 1000.0)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Yield Prediction")
    # මෙතැනදී තමයි උඹේ අදහස අනුව Prediction එක වෙන්නේ
    # දැනට අපි උදාහරණයක් විදිහට Calculation එකක් දාමු (Model එක අනුව මේක වෙනස් වෙයි)
    prediction = (rainfall * 0.5) + (temp * 0.2) - (pesticides * 0.01) 
    st.metric(label="අපේක්ෂිත අස්වැන්න (hg/ha)", value=f"{prediction:,.2f}")

with col2:
    st.subheader("💡 Smart Recommendations")
    # උඹේ අදහස: අස්වැන්න අනුව දිය යුතු උපදෙස්
    if prediction < 1000:
        st.warning("අස්වැන්න අඩුයි. වර්ෂාපතනය මදි නම් ජල සම්පාදනය වැඩි කරන්න.")
    elif prediction > 3000:
        st.success("ඉතා හොඳ අස්වැන්නක්! පළිබෝධනාශක භාවිතය සීමා කරමින් මෙය පවත්වා ගන්න.")
    
    # "What-if" අදහස ක්‍රියාත්මක කිරීම
    target_yield = st.number_input("ඔබට අවශ්‍ය ඉලක්කගත අස්වැන්න ඇතුළත් කරන්න:", value=2000)
    st.info(f"එම අස්වැන්න ලබා ගැනීමට වර්ෂාපතනය අවම වශයෙන් {(target_yield/0.5):,.1f} mm විය යුතුය.")

st.markdown("---")
st.write("© 2026 Agri-Intel Predictor | Powered by Machine Learning")